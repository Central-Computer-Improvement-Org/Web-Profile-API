from rest_framework.exceptions import AuthenticationFailed, NotFound, PermissionDenied, MethodNotAllowed, \
    NotAuthenticated, ParseError
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
            'name': exc.__class__.__name__,
            'message': exc.default_detail,
            'validation': None,
        }).data
    })

    return Response(response.data, status=status.HTTP_401_UNAUTHORIZED)


def validation_exception_handler(request, exc: ValidationError):
    val_errors = []

    if not hasattr(exc, 'detail'):
        val_errors.append(ValidationErrorSerializer({
            'name': 'Validation Error',
            'message': 'Validation error occurred'
        }).data)
    else:
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
            'message': exc.default_detail if hasattr(exc, 'default_detail') else exc,
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


def method_not_allowed_exception_handler(request, exc):
    response = ResponseSerializer({
        'code': 405,
        'status': 'METHOD_NOT_ALLOWED',
        'recordsTotal': 0,
        'error': GenericErrorSerializer({
            'name': exc.__class__.__name__,
            'message': exc.detail,
            'validation': None,
        }).data
    })

    return Response(response.data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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

    err_map = {
        'ValidationError': validation_exception_handler,
        'AuthenticationFailed': jwt_exception_handler,
        'InvalidToken': jwt_exception_handler,
        'TokenError': jwt_exception_handler,
        'NotFound': not_found_exception_handler,
        'PermissionDenied': jwt_exception_handler,
        'ValueError': bad_request_exception_handler,
        'ObjectDoesNotExist': not_found_exception_handler,
        'NotAuthenticated': unauthorized_exception_handler,
        'ParseError': bad_request_exception_handler,
        'Http404': not_found_exception_handler,
        'DoesNotExist': not_found_exception_handler,
        'MethodNotAllowed': method_not_allowed_exception_handler,
    }

    response = err_map.get(exc.__class__.__name__, server_error_exception_handler)(request, exc)

    return response
