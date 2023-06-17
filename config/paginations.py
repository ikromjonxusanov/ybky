from collections import OrderedDict
from rest_framework import pagination

from rest_framework.response import Response


class PageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page', int(self.request.query_params.get('page', 1))),
            ('count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('next', self.page.next_page_number() if self.page.has_next() else None),
            ('previous', self.page.previous_page_number() if self.page.has_previous() else None),
            ('results', data)
        ]))
