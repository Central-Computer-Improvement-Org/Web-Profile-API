from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.response import Response
from rest_framework import status

from generic_serializers.serializers import ResponseSerializer, GenericErrorSerializer, ValidationErrorSerializer


def jwt_exception_handler(exc, exception):
    error_status = "AUTH_ERROR"
    error_name = "Authentication Error"
    error_message = 'Authentication credentials were not provided or data is invalid.'

    response_status = status.HTTP_401_UNAUTHORIZED

    if isinstance(exc, TokenError) or isinstance(exc, InvalidToken):
        error_status = "TOKEN_ERROR"
        error_name = "Token Error"
        error_message = 'Token is invalid or expired.'

    serializer = ResponseSerializer({
        'code': response_status,
        'status': error_status,
        'recordsTotal': 0,
        'data': None,
        'error': {
            'name': error_name,
            'message': error_message,
            'validation': None,
        }
    })
    return Response(serializer.data)


def not_found_exception_handler(request, name):
    error_status = "NOT_FOUND_ERROR"

    response_status = status.HTTP_404_NOT_FOUND


    serializer = ResponseSerializer({
        'code': response_status,
        'status': error_status,
        'recordsTotal': 0,
        'data': None,
        'error': {
            'name': name,
            'message': name + " not found.",
            'validation': None,
        }
    })
    return Response(serializer.data)


def server_error_exception_handler(request, exception):
    error_status = "SERVER_ERROR"
    error_name = "Server Error"
    error_message = 'Internal server error.'

    response_status = status.HTTP_500_INTERNAL_SERVER_ERROR

    serializer = ResponseSerializer({
        'code': response_status,
        'status': error_status,
        'recordsTotal': 0,
        'data': None,
        'error': {
            'name': error_name,
            'message': error_message,
            'validation': None,
        }
    })
    return Response(serializer.data)


def validation_exception_handler(request, exception):
    error_status = "VALIDATION_ERROR"
    error_name = "Validation Error"
    error_message = 'Validation error.'

    response_status = status.HTTP_400_BAD_REQUEST

    val_errors = []

    for key, value in exception.items():
        val_errors.append(ValidationErrorSerializer({
            'name': f"{key} field error",
            'message': str(value[0]),
        }).data)

    serializer = ResponseSerializer({
        'code': response_status,
        'status': error_status,
        'recordsTotal': 0,
        'data': None,
        'error': GenericErrorSerializer(
            {
                "name": error_name,
                "message": error_message,
                "validation": ValidationErrorSerializer(val_errors, many=True).data
            }
        ).data,
    })
    return Response(serializer.data)


def bad_request_exception_handler(request, name, message):
    error_status = "BAD_REQUEST_ERROR"

    response_status = status.HTTP_400_BAD_REQUEST

    serializer = ResponseSerializer({
        'code': response_status,
        'status': error_status,
        'recordsTotal': 0,
        'data': None,
        'error': {
            'name': name,
            'message': message,
            'validation': None,
        }
    })
    return Response(serializer.data)
