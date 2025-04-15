
from django.urls import path,include
from common.views import CommonApi
from rest_framework.routers import DefaultRouter
from common.views import AssignGroupApi,AssignPermissionApi,CustomTokenObtainPairView

# for the token based authentication
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

# from common.viewsa import CustomTokenObtainView, RefreshAccessTokenView 


# router=DefaultRouter()
# router.register("commonapi",CommonApi,basename='combined')
# router.register('permission',AssignPermissionApi,basename="permission")
# router.register('group',AssignGroupApi,basename='group')

urlpatterns = [
    # path('api/',include(router.urls)),
    path("gettoken",TokenObtainPairView.as_view(),name="token_obtain_view"),
    path("refreshtoken",TokenRefreshView.as_view(),name="token_refresh"),
    path("verifytoken",TokenVerifyView.as_view(),name="token_verify"),
    path("common/gettoken", CustomTokenObtainPairView.as_view(), name="token_obtain_view"),
    path("api/all",CommonApi.as_view(),name='common')

]
