# from user.views import data
from django.urls import path
from user.views import get_user_profile,change_password


urlpatterns = [
        
path("info/",get_user_profile,name="userInfo"),
path("changePassword/",change_password,name="changepassword"),


]
