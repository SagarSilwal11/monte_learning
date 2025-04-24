from django.urls import path
from testimonials.views import TestimonialsApi
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('testimonials', TestimonialsApi.as_view(), name='test-list'), 
    path('testimonial/<int:pk>', TestimonialsApi.as_view(), name='test-get'), 
    path('testimonial/create', TestimonialsApi.as_view(), name='test-create'),  
    path('testimonial/update/<int:pk>', TestimonialsApi.as_view(), name='test-update'), 
    path('testimonial/patch/<int:pk>', TestimonialsApi.as_view(), name='test-patch'),  
    path('testimonial/delete/<int:pk>', TestimonialsApi.as_view(), name='test-delete'), 
]
