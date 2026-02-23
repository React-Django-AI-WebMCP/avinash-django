import logging

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


class ApplicationError(APIException):
    """Raised for domain / business rule violations (400)."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A business rule was violated."
    default_code = "application_error"


class ConflictError(APIException):
    """Raised when a resource already exists (409)."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = "Resource already exists."
    default_code = "conflict"


class ServiceUnavailableError(APIException):
    """Raised when a downstream service is unreachable (503)."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Service temporarily unavailable."
    default_code = "service_unavailable"


def custom_exception_handler(exc, context):
    """
    Wraps DRF's default exception handler to produce a uniform response shape:
      { success: false, message: "...", errors: {...} }
    """
    if isinstance(exc, Http404):
        exc = APIException(detail="Not found.")
        exc.status_code = status.HTTP_404_NOT_FOUND

    elif isinstance(exc, PermissionDenied):
        exc = APIException(detail="Permission denied.")
        exc.status_code = status.HTTP_403_FORBIDDEN

    elif isinstance(exc, ValidationError):
        exc = APIException(detail=exc.message_dict if hasattr(exc, "message_dict") else str(exc))
        exc.status_code = status.HTTP_400_BAD_REQUEST

    response = exception_handler(exc, context)

    if response is not None:
        original_data = response.data
        errors = None

        if isinstance(original_data, dict):
            message = original_data.pop("detail", "An error occurred.")
            errors = original_data if original_data else None
        elif isinstance(original_data, list):
            message = "Validation error."
            errors = original_data
        else:
            message = str(original_data)

        response.data = {
            "success": False,
            "message": str(message),
        }
        if errors:
            response.data["errors"] = errors

        if response.status_code >= 500:
            logger.error("5xx error: %s | context: %s", exc, context)

    return response
