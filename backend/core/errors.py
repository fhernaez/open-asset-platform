"""Unified problem-details error handling and domain exceptions."""

from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


class OAPError(Exception):
    """Base domain error carrying an HTTP status and a machine-readable code."""

    status_code = status.HTTP_400_BAD_REQUEST
    code = "bad_request"

    def __init__(self, detail: str, *, code: str | None = None, status_code: int | None = None):
        self.detail = detail
        if code is not None:
            self.code = code
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail)


class NotFoundError(OAPError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"


class PermissionDeniedError(OAPError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "forbidden"


class ConflictError(OAPError):
    status_code = status.HTTP_409_CONFLICT
    code = "conflict"


class ValidationError(OAPError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = "validation_error"


class DependencyUnavailableError(OAPError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "dependency_unavailable"


def _problem(status_code: int, code: str, detail: str) -> Response:
    return Response(
        {"type": "about:blank", "title": code.replace("_", " "), "status": status_code, "detail": detail},
        status=status_code,
    )


def api_exception_handler(exc, context):
    if isinstance(exc, OAPError):
        return _problem(exc.status_code, exc.code, exc.detail)
    if isinstance(exc, DjangoValidationError):
        return _problem(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "validation_error", exc.messages[0] if exc.messages else str(exc)
        )
    if isinstance(exc, IntegrityError):
        return _problem(status.HTTP_409_CONFLICT, "conflict", "Resource conflicts with an existing record.")
    response = drf_exception_handler(exc, context)
    return response
