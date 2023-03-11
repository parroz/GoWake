from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class CompetitionsAppPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 1
    last_page_strings = 'end'