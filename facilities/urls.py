from django.urls import path
from facilities.views import FacilityApi

urlpatterns = [
    # path('facilityapi/', FacilityApi.as_view(), name='facility-list'),  # List and create facilities
    # path('facilityapi/<int:pk>/', FacilityApi.as_view(), name='facility-detail'),  # Retrieve, update, delete

    path('facilityapi/', FacilityApi.as_view(), name='facility-list'),  
    path('facilityapi/<int:pk>/', FacilityApi.as_view(), name='facility-get'),  
    path('facilityapi/create/', FacilityApi.as_view(), name='facility-create'),  
    path('facilityapi/update/<int:pk>/', FacilityApi.as_view(), name='facility-update'),  
    path('facilityapi/patch/<int:pk>/', FacilityApi.as_view(), name='facility-patch'), 
    path('facilityapi/delete/<int:pk>/', FacilityApi.as_view(), name='facility-delete'),
    
]
