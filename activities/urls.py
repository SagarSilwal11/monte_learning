from django.urls import path
from activities.views import ActivityApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
   

    path('activityapi', ActivityApi.as_view(), name='activity-list'),
    # path('activityapi/<int:pk>/', ActivityApi.as_view(), name='activity-detail'),
    path("activityapi/<int:pk>",ActivityApi.as_view(),name="activity_list"),
    path("activityapi/create",ActivityApi.as_view(),name="activity_create"),
    path("activityapi/update/<int:pk>",ActivityApi.as_view(),name="activity_update"),
    path("activityapi/patch/<int:pk>",ActivityApi.as_view(),name="activity_updates"),
    path("activityapi/delete/<int:pk>",ActivityApi.as_view(),name="activity_delete"),

]
