"""Pub/Sub message schemas for pipeline events.

Each function in the pipeline publishes messages to the next stage.
These Pydantic models define the contract between functions.
"""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from shared.schemas.invoice import VendorType


class InvoiceUploadedMessage(BaseModel):
    """Message published when TIFF lands in input bucket (GCS notification)."""

    bucket: str = Field(..., description="GCS bucket name")
    name: str = Field(..., description="File path in bucket")
    event_time: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")


class InvoiceConvertedMessage(BaseModel):
    """Message published after TIFF to PNG conversion."""

    source_file: str = Field(..., description="gs:// URI of original TIFF")
    converted_files: list[str] = Field(..., description="List of gs:// URIs for PNGs")
    page_count: int = Field(..., ge=1, description="Number of pages converted")
    event_time: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")


class InvoiceClassifiedMessage(BaseModel):
    """Message published after vendor classification."""

    source_file: str = Field(..., description="gs:// URI of original TIFF")
    converted_files: list[str] = Field(..., description="List of gs:// URIs for PNGs")
    vendor_type: VendorType = Field(..., description="Detected vendor type")
    quality_score: float = Field(..., ge=0.0, le=1.0, description="Image quality score")
    archived_to: str = Field(..., description="gs:// URI in archive bucket")
    event_time: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")


class InvoiceExtractedMessage(BaseModel):
    """Message published after LLM extraction."""

    source_file: str = Field(..., description="gs:// URI of original TIFF")
    vendor_type: VendorType = Field(..., description="Vendor type")
    extraction_model: Literal["gemini-2.5-flash", "openrouter"] = Field(
        ..., description="Model used for extraction"
    )
    extraction_latency_ms: int = Field(..., ge=0, description="Extraction latency")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Extraction confidence")
    extracted_data: dict[str, Any] = Field(..., description="ExtractedInvoice as dict")
    event_time: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
