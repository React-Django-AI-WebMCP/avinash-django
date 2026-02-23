from typing import Any

from rest_framework import status
from rest_framework.response import Response


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = status.HTTP_200_OK,
    meta: dict | None = None,
) -> Response:
    payload: dict[str, Any] = {
        "success": True,
        "message": message,
        "data": data,
    }
    if meta is not None:
        payload["meta"] = meta
    return Response(payload, status=status_code)


def created_response(data: Any = None, message: str = "Created successfully") -> Response:
    return success_response(data=data, message=message, status_code=status.HTTP_201_CREATED)


def no_content_response(message: str = "Deleted successfully") -> Response:
    return Response({"success": True, "message": message}, status=status.HTTP_204_NO_CONTENT)


def error_response(
    message: str = "An error occurred",
    errors: Any = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    payload: dict[str, Any] = {
        "success": False,
        "message": message,
    }
    if errors is not None:
        payload["errors"] = errors
    return Response(payload, status=status_code)
