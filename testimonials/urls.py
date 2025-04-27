from django.urls import path
from testimonials.views import TestimonialsApi
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('testimonialapi', TestimonialsApi.as_view(), name='test-list'), 
    path('testimonialapi/<int:pk>', TestimonialsApi.as_view(), name='test-get'), 
    path('testimonialapi/create', TestimonialsApi.as_view(), name='test-create'),  
    path('testimonialapi/update/<int:pk>', TestimonialsApi.as_view(), name='test-update'), 
    path('testimonialapi/patch/<int:pk>', TestimonialsApi.as_view(), name='test-patch'),  
    path('testimonialapi/delete/<int:pk>', TestimonialsApi.as_view(), name='test-delete'), 
]