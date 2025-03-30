from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash,password_validation
# Create your views here.

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):

    user=request.user
    print("User",user)
    print("Is Authenticated:",request.user.is_authenticated)
    if user.is_authenticated:
        return Response({
            'username':user.username,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "email":user.email,
            "last_login":user.last_login,
            "date_joined":user.date_joined

        })
    return Response({"message":"User Authentication Failed"},status=403)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user=request.user
    old_password=request.data.get("old_password")
    new_password=request.data.get("new_password")
    confirm_password=request.data.get("confirm_password")
    if not user.check_password(old_password):
        return Response({'message':'Old password is incorrect'},status=status.HTTP_400_BAD_REQUEST)
    
    if new_password!=confirm_password:
        return Response({'error':'Password must be at least 8 characters long '},status=status.HTTP_400_BAD_REQUEST)
    
    try:
        password_validation.validate_password(new_password,user)
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request,user)
    return Response({"message":"Password change sucessfully"},status=status.HTTP_200_OK)