from django.contrib import admin
from django.urls import path,include
from hero.views import HeroApi
from rest_framework.routers import DefaultRouter
from hero.models import Hero

# router=DefaultRouter()
# router.register("heroapi",HeroApi,basename='hero')



# urlpatterns = [
#     path('api/',include(router.urls)),
  
# ]

from django.urls import path
from .views import HeroApi

urlpatterns = [
    path('heroapi/', HeroApi.as_view(), name='hero-list'), 
    path('heroapi/<int:pk>/', HeroApi.as_view(), name='hero-get'), 
    path('heroapi/create/', HeroApi.as_view(), name='hero-create'),  
    path('heroapi/update/<int:pk>/', HeroApi.as_view(), name='hero-update'), 
    path('heroapi/patch/<int:pk>/', HeroApi.as_view(), name='hero-patch'),  
    path('heroapi/delete/<int:pk>/', HeroApi.as_view(), name='hero-delete'), 
]

