from rest_framework.pagination import PageNumberPagination
from math import ceil
from rest_framework.response import Response
class CustomPageNumberPagination(PageNumberPagination):
    page_size=5
    page_size_query_param="page_size"
    max_page_size=50

    def get_paginated_response(self, data):
        page_size=self.get_page_size(self.request)
        total=ceil(self.page.paginator.count/page_size)
        current_page=self.page.number
        return Response({
            'count': self.page.paginator.count,  
            'next': self.get_next_link(),
            'previous': self.get_previous_link(), 
            'total_pages': total,
            'page_size': page_size,  
            'current_page': current_page,  
            'results': data  
        })

     