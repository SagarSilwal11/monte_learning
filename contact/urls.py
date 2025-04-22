
from django.urls import path,include
from contact.views import ContactApi
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView,TokenVerifyView
from contact.views import ContactApi






urlpatterns = [

    # path('contactapi/',ContactApi.as_view(),name='contact-list'),
    # path('contactapi/<int:pk>/',ContactApi.as_view(),name='contact'),
    path("contactapi",ContactApi.as_view(),name="contact_list"),
    path("contactapi/<int:pk>",ContactApi.as_view(),name="activity_list"),
    path("contactapi/create",ContactApi.as_view(),name="activity_create"),
    path("contactapi/put/<int:pk>",ContactApi.as_view(),name="activity_update"),
    path("contactapi/patch/<int:pk>",ContactApi.as_view(),name="activity_updates"),
    path("contactapi/delete/<int:pk>",ContactApi.as_view(),name="activity_delete"),

]
