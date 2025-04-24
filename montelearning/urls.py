
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

from facilities.views import FacilityApi
from about.views import AboutApi
from career.views import CareerModelApi
from activities.views import ActivityApi




urlpatterns = [

    path("admin/", admin.site.urls),
    path('hero/',include('hero.urls')),
    path('activity/',include('activities.urls')),
    path("facility/",include('facilities.urls')),
    path('contact/',include('contact.urls')),
    path('common/',include('common.urls')),  
    path('user/',include('user.urls')),
    path('testimonial/',include('testimonials.urls')),

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
