"""Invoice data extraction using LLM.

Orchestrates the extraction process:
1. Load vendor-specific prompt template
2. Call Gemini via Vertex AI
3. Parse and validate JSON response
4. Fallback to OpenRouter on failure
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from shared.adapters.llm import LLMAdapter, LLMResponse
from shared.schemas.invoice import ExtractedInvoice, VendorType

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).parent / "prompts"


@dataclass
class InvoiceExtractionResult:
    """Result of invoice extraction.

    Attributes:
        success: Whether extraction succeeded
        invoice: Extracted invoice data (if successful)
        provider: LLM provider used (gemini or openrouter)
        latency_ms: Total extraction latency in milliseconds
        confidence: Extraction confidence score
        error: Error message (if failed)
        raw_response: Raw LLM response for debugging
    """

    success: bool
    invoice: ExtractedInvoice | None
    provider: Literal["gemini", "openrouter"]
    latency_ms: int
    confidence: float
    error: str | None = None
    raw_response: str | None = None


def extract_invoice(
    images_data: list[bytes],
    vendor_type: VendorType,
    llm_adapter: LLMAdapter,
    fallback_adapter: LLMAdapter | None = None,
) -> InvoiceExtractionResult:
    """Extract structured data from invoice images.

    Uses vendor-specific prompt for better accuracy. Attempts primary
    LLM first, falls back to secondary on failure.

    Args:
        images_data: List of PNG image bytes (one per page)
        vendor_type: Detected vendor type for prompt selection
        llm_adapter: Primary LLM adapter (Gemini)
        fallback_adapter: Optional fallback LLM adapter (OpenRouter)

    Returns:
        InvoiceExtractionResult with extracted invoice or error details
    """
    prompt = load_prompt_template(vendor_type)

    result = _try_extraction(images_data, prompt, llm_adapter, "gemini")
    if result.success:
        return result

    logger.warning(
        "Primary extraction failed, attempting fallback",
        extra={
            "vendor_type": vendor_type.value,
            "primary_error": result.error,
        },
    )

    if fallback_adapter:
        fallback_result = _try_extraction(
            images_data, prompt, fallback_adapter, "openrouter"
        )
        if fallback_result.success:
            return fallback_result

        return InvoiceExtractionResult(
            success=False,
            invoice=None,
            provider="openrouter",
            latency_ms=result.latency_ms + fallback_result.latency_ms,
            confidence=0.0,
            error=f"Both providers failed. Primary: {result.error}. Fallback: {fallback_result.error}",
            raw_response=fallback_result.raw_response,
        )

    return result


def _try_extraction(
    images_data: list[bytes],
    prompt: str,
    llm_adapter: LLMAdapter,
    provider: Literal["gemini", "openrouter"],
) -> InvoiceExtractionResult:
    """Attempt extraction with a single LLM provider.

    Args:
        images_data: List of PNG image bytes
        prompt: Prompt template with schema
        llm_adapter: LLM adapter to use
        provider: Provider name for logging

    Returns:
        InvoiceExtractionResult with outcome
    """
    try:
        response: LLMResponse = llm_adapter.extract(
            prompt=prompt,
            image_data=images_data,
        )

        if not response.success:
            return InvoiceExtractionResult(
                success=False,
                invoice=None,
                provider=provider,
                latency_ms=response.latency_ms,
                confidence=0.0,
                error=response.error_message or "LLM extraction failed",
                raw_response=response.content,
            )

        invoice = _parse_and_validate(response.content)

        return InvoiceExtractionResult(
            success=True,
            invoice=invoice,
            provider=provider,
            latency_ms=response.latency_ms,
            confidence=0.9,  # Default confidence for successful extractions
            raw_response=response.content,
        )

    except json.JSONDecodeError as e:
        return InvoiceExtractionResult(
            success=False,
            invoice=None,
            provider=provider,
            latency_ms=response.latency_ms if "response" in dir() else 0,
            confidence=0.0,
            error=f"JSON parse error: {e}",
            raw_response=response.content if "response" in dir() else None,
        )

    except ValueError as e:
        return InvoiceExtractionResult(
            success=False,
            invoice=None,
            provider=provider,
            latency_ms=response.latency_ms if "response" in dir() else 0,
            confidence=0.0,
            error=f"Validation error: {e}",
            raw_response=response.content if "response" in dir() else None,
        )

    except Exception as e:
        logger.exception(f"Unexpected extraction error with {provider}")
        return InvoiceExtractionResult(
            success=False,
            invoice=None,
            provider=provider,
            latency_ms=0,
            confidence=0.0,
            error=f"Unexpected error: {e}",
        )


def _parse_and_validate(content: str) -> ExtractedInvoice:
    """Parse LLM response and validate with Pydantic.

    Handles common LLM response issues:
    - Markdown code blocks (```json ... ```)
    - Leading/trailing whitespace
    - Minor JSON formatting issues

    Args:
        content: Raw LLM response text

    Returns:
        Validated ExtractedInvoice

    Raises:
        json.JSONDecodeError: If content is not valid JSON
        ValueError: If JSON doesn't match ExtractedInvoice schema
    """
    cleaned = content.strip()

    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        start_idx = 1 if lines[0].startswith("```") else 0
        end_idx = -1 if lines[-1].strip() == "```" else len(lines)
        cleaned = "\n".join(lines[start_idx:end_idx]).strip()

    data = json.loads(cleaned)

    try:
        return ExtractedInvoice.model_validate(data)
    except Exception as e:
        raise ValueError(f"Schema validation failed: {e}") from e


def load_prompt_template(vendor_type: VendorType) -> str:
    """Load vendor-specific prompt template.

    Falls back to generic template if vendor-specific not found.

    Args:
        vendor_type: Vendor type for template selection

    Returns:
        Prompt template with {schema} placeholder
    """
    vendor_file = PROMPTS_DIR / f"{vendor_type.value}.txt"

    if vendor_file.exists():
        template = vendor_file.read_text()
        logger.debug(f"Loaded prompt template: {vendor_file.name}")
    else:
        generic_file = PROMPTS_DIR / "generic.txt"
        template = generic_file.read_text()
        logger.info(
            f"No template for {vendor_type.value}, using generic",
            extra={"vendor_type": vendor_type.value},
        )

    schema = ExtractedInvoice.model_json_schema()
    return template.replace("{schema}", json.dumps(schema, indent=2))


def get_available_prompts() -> list[str]:
    """List available prompt templates.

    Returns:
        List of vendor types with available prompts
    """
    return [f.stem for f in PROMPTS_DIR.glob("*.txt")]
