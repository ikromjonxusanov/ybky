from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import exception_handler

from room.exceptions import HttpGone


def handler(exc, context):
    if isinstance(exc, Http404):
        return Response({"error": "topilmadi"}, status=404)
    if isinstance(exc, HttpGone):
        return Response({"error": "uzr, siz tanlagan vaqtda xona band"}, status=410)

    response = exception_handler(exc, context)

    if response is None:
        raise exc

    return response
