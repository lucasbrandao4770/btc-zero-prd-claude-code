"""Cloud Run entry point for BigQuery writer.

Triggered by Pub/Sub messages on the invoice-extracted topic.
Validates extracted data, checks for duplicates, writes to BigQuery,
and logs extraction metrics.
"""

import base64
import json
import logging

import functions_framework
from cloudevents.http import CloudEvent

from shared.adapters import GCPBigQueryAdapter, PubSubAdapter
from shared.schemas.invoice import ExtractedInvoice
from shared.schemas.messages import InvoiceExtractedMessage
from shared.utils import configure_logging, get_config

from .writer import write_extraction_metrics, write_invoice_to_bigquery

configure_logging()
logger = logging.getLogger(__name__)


@functions_framework.cloud_event
def handle_invoice_extracted(cloud_event: CloudEvent) -> None:
    """Cloud Run entry point - triggered by Pub/Sub.

    Processes extracted invoices by:
    1. Re-validating extracted data with Pydantic (defense in depth)
    2. Checking for duplicate invoices
    3. Writing invoice and line items to BigQuery
    4. Logging extraction metrics

    Args:
        cloud_event: CloudEvent containing Pub/Sub message with:
            - source_file: GCS URI of original file
            - vendor_type: Detected vendor type
            - extraction_model: LLM model used
            - extraction_latency_ms: Processing time
            - confidence_score: Extraction confidence
            - extracted_data: Invoice data as dict

    Raises:
        Exception: Re-raised to trigger Cloud Run retry on failure
    """
    config = get_config()
    bq_adapter = GCPBigQueryAdapter(project_id=config.project_id)

    source_file = "unknown"
    invoice_id = "unknown"

    try:
        message_data = base64.b64decode(cloud_event.data["message"]["data"])
        raw_message = json.loads(message_data)

        message = InvoiceExtractedMessage.model_validate(raw_message)
        source_file = message.source_file

        logger.info(
            "Processing extracted invoice",
            extra={
                "source_file": source_file,
                "vendor_type": message.vendor_type.value,
                "extraction_model": message.extraction_model,
                "confidence_score": message.confidence_score,
            },
        )

        invoice = ExtractedInvoice.model_validate(message.extracted_data)
        invoice_id = invoice.invoice_id

        logger.info(
            "Invoice re-validated successfully",
            extra={
                "invoice_id": invoice_id,
                "vendor_type": invoice.vendor_type.value,
                "line_items_count": len(invoice.line_items),
                "total_amount": str(invoice.total_amount),
            },
        )

        result = write_invoice_to_bigquery(
            invoice=invoice,
            bq_adapter=bq_adapter,
            dataset=config.dataset,
            invoices_table=config.invoices_table,
            line_items_table=config.line_items_table,
            source_file=source_file,
            extraction_model=message.extraction_model,
            extraction_latency_ms=message.extraction_latency_ms,
            confidence_score=message.confidence_score,
        )

        if not result.success:
            logger.error(
                "BigQuery write failed",
                extra={
                    "invoice_id": invoice_id,
                    "error": result.error,
                },
            )
            raise RuntimeError(f"BigQuery write failed: {result.error}")

        write_extraction_metrics(
            bq_adapter=bq_adapter,
            dataset=config.dataset,
            metrics_table=config.metrics_table,
            invoice_id=invoice_id,
            vendor_type=message.vendor_type,
            source_file=source_file,
            extraction_model=message.extraction_model,
            extraction_latency_ms=message.extraction_latency_ms,
            confidence_score=message.confidence_score,
            success=True,
        )

        if result.is_duplicate:
            logger.info(
                "Duplicate invoice - no action taken",
                extra={
                    "invoice_id": invoice_id,
                    "source_file": source_file,
                },
            )
        else:
            logger.info(
                "Invoice persisted to BigQuery",
                extra={
                    "invoice_id": invoice_id,
                    "vendor_type": invoice.vendor_type.value,
                    "rows_written": result.rows_written,
                    "dataset": config.dataset,
                    "table": config.invoices_table,
                },
            )

    except Exception as e:
        logger.exception(
            "BigQuery write processing failed",
            extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "source_file": source_file,
                "invoice_id": invoice_id,
            },
        )

        try:
            write_extraction_metrics(
                bq_adapter=bq_adapter,
                dataset=config.dataset,
                metrics_table=config.metrics_table,
                invoice_id=invoice_id,
                vendor_type=message.vendor_type if "message" in dir() else "other",
                source_file=source_file,
                extraction_model=message.extraction_model if "message" in dir() else "unknown",
                extraction_latency_ms=message.extraction_latency_ms if "message" in dir() else 0,
                confidence_score=0.0,
                success=False,
                error_message=str(e),
            )
        except Exception:
            pass

        raise
