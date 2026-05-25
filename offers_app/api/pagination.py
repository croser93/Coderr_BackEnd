from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    """
    Custom Pagination for GET /api/offers/ Endpoint.
    
    page_size = How many elements in 1 page.
    page_size_query_param = 'page_size'
    max_page_size = Max Page size.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100