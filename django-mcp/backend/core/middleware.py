import logging
import time
import uuid

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """Logs every inbound request with method, path, status, duration, and user."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        request.META["HTTP_X_REQUEST_ID"] = request_id

        start = time.monotonic()
        response = self.get_response(request)
        duration_ms = round((time.monotonic() - start) * 1000, 2)

        user = getattr(request, "user", None)
        user_id = user.pk if user and user.is_authenticated else "anonymous"

        logger.info(
            "request",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.get_full_path(),
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "user_id": str(user_id),
            },
        )
        response["X-Request-ID"] = request_id
        return response
