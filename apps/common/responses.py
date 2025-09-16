"""
Standardized API response formats for consistency across the entire codebase.
Inspired by FastAPI response patterns with Django REST Framework integration.
"""

from typing import Any

from rest_framework import status
from rest_framework.response import Response


class APIResponse:
    """
    Consistent API response structure following REST best practices.

    All API responses follow this structure:
    {
        "success": bool,
        "message": str,
        "data": Any,
        "error": Optional[Dict],
        "metadata": Dict
    }
    """

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Operation completed successfully",
        status_code: int = status.HTTP_200_OK,
        metadata: dict[str, Any] | None = None,
    ) -> Response:
        """
        Standard success response.

        Args:
            data: Response payload
            message: Human-readable success message
            status_code: HTTP status code
            metadata: Additional metadata (pagination, etc.)

        Returns:
            DRF Response object with standardized structure
        """
        response_data = {
            "success": True,
            "message": message,
            "data": data,
            "error": None,
            "metadata": metadata or {},
        }
        return Response(response_data, status=status_code)

    @staticmethod
    def error(
        message: str = "An error occurred",
        errors: list[str] | dict[str, Any] | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str | None = None,
    ) -> Response:
        """
        Standard error response.

        Args:
            message: Human-readable error message
            errors: Detailed error information
            status_code: HTTP status code
            error_code: Machine-readable error code

        Returns:
            DRF Response object with error structure
        """
        response_data = {
            "success": False,
            "message": message,
            "data": None,
            "error": {
                "code": error_code or f"ERROR_{status_code}",
                "details": errors or [],
            },
            "metadata": {},
        }
        return Response(response_data, status=status_code)

    @staticmethod
    def validation_error(
        field_errors: dict[str, list[str]], message: str = "Validation failed"
    ) -> Response:
        """
        Standardized validation error response.

        Args:
            field_errors: Dictionary of field-specific errors
            message: General validation error message

        Returns:
            Validation error response
        """
        return APIResponse.error(
            message=message,
            errors=field_errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
        )

    @staticmethod
    def not_found(
        resource: str = "Resource", identifier: str | None = None
    ) -> Response:
        """
        Standardized 404 response.

        Args:
            resource: Type of resource not found
            identifier: Specific identifier that wasn't found

        Returns:
            404 error response
        """
        message = f"{resource} not found"
        if identifier:
            message += f" with identifier: {identifier}"

        return APIResponse.error(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND",
        )

    @staticmethod
    def unauthorized(message: str = "Authentication required") -> Response:
        """Standardized 401 response."""
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
        )

    @staticmethod
    def forbidden(message: str = "Insufficient permissions") -> Response:
        """Standardized 403 response."""
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
        )
