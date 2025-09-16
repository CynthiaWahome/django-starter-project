"""
Unit tests for common response utilities.
"""

from rest_framework import status

from apps.common.responses import APIResponse


class TestAPIResponse:
    """Test APIResponse utility class."""

    def test_success_response_structure(self):
        """Test success response has correct structure."""
        response = APIResponse.success(data={"key": "value"}, message="Test success")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == "Test success"
        assert response.data["data"] == {"key": "value"}
        assert response.data["error"] is None
        assert "metadata" in response.data

    def test_error_response_structure(self):
        """Test error response has correct structure."""
        response = APIResponse.error(message="Test error", error_code="TEST_ERROR")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert response.data["message"] == "Test error"
        assert response.data["data"] is None
        assert response.data["error"]["code"] == "TEST_ERROR"

    def test_validation_error_response(self):
        """Test validation error response."""
        field_errors = {
            "email": ["This field is required."],
            "password": ["Password too weak."],
        }

        response = APIResponse.validation_error(field_errors)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.data["error"]["code"] == "VALIDATION_ERROR"
        assert response.data["error"]["details"] == field_errors

    def test_not_found_response(self):
        """Test not found response."""
        response = APIResponse.not_found("User", "123")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found with identifier: 123" in response.data["message"]
