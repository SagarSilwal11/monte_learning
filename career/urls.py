
from django.urls import path,include
from career.views import CareerModelApi
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView,TokenVerifyView



router=DefaultRouter()
router.register("careerapi",CareerModelApi,basename='career')



urlpatterns = [
    path('api/',include(router.urls)),
    path("careertokengen/",TokenObtainPairView.as_view(),name='htoken'),
    path("careertokenrefresh/",TokenRefreshView.as_view(),name='htoken'),
    path('careertokenverify/',TokenVerifyView.as_view(),name='htokenverify')

]
