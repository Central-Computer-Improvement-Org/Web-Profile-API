from django.http import JsonResponse, Http404

from generic_serializers.serializers import ResponseSerializer, GenericErrorSerializer


def error_404(request, exception: Http404):
    return JsonResponse(
        ResponseSerializer({
            'code': 404,
            'status': 'NOT_FOUND_ERROR',
            'recordsTotal': 0,
            'data': None,
            'error': GenericErrorSerializer({
                'name': 'Not Found',
                'message': 'Resource not found',
                'validation': None,
            }).data
        }).data
    )