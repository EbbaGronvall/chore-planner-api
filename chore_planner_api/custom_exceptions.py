from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Custom exception handler to provide standardized error responses.
    """
    
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        return Response(
            {"error": "Validation failed", "details": exc.message_dict},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, APIException):
        return Response(
            {"error": exc.detail},
            status=exc.status_code
        )

    if response is None:
        return Response(
            {"error": "A server error occurred. Please try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
