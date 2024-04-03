from rest_framework.exceptions import AuthenticationFailed, NotFound, PermissionDenied, NotAuthenticated, ParseError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.response import Response
from rest_framework import status

from rest_framework.exceptions import ValidationError

from generic_serializers.serializers import ResponseSerializer, GenericErrorSerializer, ValidationErrorSerializer

from django.db.models import ObjectDoesNotExist

from django.http import Http404

def jwt_exception_handler(request, exc):
    response = ResponseSerializer({
        'code': 401,
        'status': 'AUTHENTICATION_ERROR',
        'recordsTotal': 0,
        'data': None,
        'error': GenericErrorSerializer({
            'name': exc.__name__,
            'message': exc.default_detail,
            'validation': None,
        }).data
    })

    return Response(response.data, status=status.HTTP_401_UNAUTHORIZED)


def validation_exception_handler(request, exc: ValidationError):
    val_errors = []

    for key, value in exc.detail.items():
        val_errors.append(ValidationErrorSerializer({
            'name': key,
            'message': value[0]
        }).data)

    response = ResponseSerializer({
        'code': 400,
        'status': 'VALIDATION_ERROR',
        'recordsTotal': 0,
        'error': GenericErrorSerializer({
            'name': exc.__class__.__name__,
            'message': exc.default_detail,
            'validation': val_errors
        }).data
    })

    return Response(response.data, status=status.HTTP_400_BAD_REQUEST)


def server_error_exception_handler(request, exc):
    response = ResponseSerializer({
        'code': 500,
        'status': 'SERVER_ERROR',
        'recordsTotal': 0,
        'error': GenericErrorSerializer({
            'name': exc.__class__.__name__,
            'message': exc.__str__(),
            'validation': None,
        }).data
    })

    return Response(response.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def unauthorized_exception_handler(request, exc):
    response = ResponseSerializer({
        'code': 401,
        'status': 'UNAUTHORIZED',
        'recordsTotal': 0,
        'error': GenericErrorSerializer({
            'name': exc.__class__.__name__,
            'message': exc.detail,
            'validation': None,
        }).data
    })

    return Response(response.data, status=status.HTTP_401_UNAUTHORIZED)


def not_found_exception_handler(request, exc):
    response = ResponseSerializer({
        'code': 404,
        'status': 'NOT_FOUND',
        'recordsTotal': 0,
        'error': GenericErrorSerializer({
            'name': exc.__class__.__name__,
            'message': exc.__str__(),
            'validation': None,
        }).data
    })

    return Response(response.data, status=status.HTTP_404_NOT_FOUND)


def bad_request_exception_handler(request, exc):
    response = ResponseSerializer({
        'code': 400,
        'status': 'BAD_REQUEST',
        'recordsTotal': 0,
        'error': GenericErrorSerializer({
            'name': exc.__class__.__name__,
            'message': exc.__str__(),
            'validation': None,
        }).data
    })

    return Response(response.data, status=status.HTTP_400_BAD_REQUEST)

def global_exception_handler(exc, context):
    request = context['request']
    response = None

    print(exc.__class__)

    if isinstance(exc, ValidationError):
        response = validation_exception_handler(request, exc)
    elif isinstance(exc, AuthenticationFailed):
        response = jwt_exception_handler(request, AuthenticationFailed)
    elif isinstance(exc, InvalidToken):
        response = jwt_exception_handler(exc, InvalidToken)
    elif isinstance(exc, TokenError):
        response = jwt_exception_handler(exc, TokenError)
    elif isinstance(exc, NotFound):
        response = not_found_exception_handler(request, exc)
    elif isinstance(exc, PermissionDenied):
        response = jwt_exception_handler(exc, PermissionDenied)
    elif isinstance(exc, ValueError):
        response = bad_request_exception_handler(request, exc)
    elif isinstance(exc, ObjectDoesNotExist):
        response = not_found_exception_handler(request, exc)
    elif isinstance(exc, NotAuthenticated):
        response = unauthorized_exception_handler(request, exc)
    elif isinstance(exc, ParseError):
        response = bad_request_exception_handler(request, exc)
    else:
        response = server_error_exception_handler(request, exc)

    return response
