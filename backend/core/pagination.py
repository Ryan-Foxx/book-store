from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param

class BasePagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 50

    def get_previous_link(self):
        if not self.page.has_previous():
            return None

        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()

        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "page_size": self.get_page_size(self.request),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
