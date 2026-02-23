import logging

from django.db import connection
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from core.responses import error_response, success_response

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    """GET /health/ — basic liveness probe."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        return success_response(data={"status": "ok"}, message="Service is healthy.")


class ReadinessCheckView(APIView):
    """GET /ready/ — readiness probe: validates DB + cache connectivity."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        checks: dict[str, str] = {}

        # Database
        try:
            connection.ensure_connection()
            checks["database"] = "ok"
        except Exception as exc:
            logger.error("Readiness check — DB failed: %s", exc)
            checks["database"] = "error"

        # Cache
        try:
            cache.set("readiness_probe", "1", timeout=5)
            assert cache.get("readiness_probe") == "1"
            checks["cache"] = "ok"
        except Exception as exc:
            logger.error("Readiness check — cache failed: %s", exc)
            checks["cache"] = "error"

        all_ok = all(v == "ok" for v in checks.values())
        if all_ok:
            return success_response(data=checks, message="Service is ready.")
        return error_response(message="Service not ready.", errors=checks, status_code=503)
