from rest_framework import status
from rest_framework.exceptions import APIException


class HttpGone(APIException):
    status_code = status.HTTP_410_GONE
    default_detail = 'uzr, siz tanlagan vaqtda xona band'
    default_code = 'uzr, siz tanlagan vaqtda xona band'
