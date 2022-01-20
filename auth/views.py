from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated , IsAdminUser

from rest_framework.response import Response

from rest_framework.views import APIView

from django.contrib.auth.models import User

from .serializers import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password

from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairSeralizer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k , v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSeralizer



class Register(APIView):
    def post(self,request):
        data = request.data

        try:
            user = User.objects.create(
                first_name = data['name'],
                username = data['username'],
                email = data['email'],
                password = make_password(data['password'])
            )
            serializer = UserSerializer(user,many=False)
            return Response(serializer.data)
        except:
            return Response({"msg":'user is already exists'})



class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        token = request.data["token"]
        data = RefreshToken(token)
        data.blacklist()
        return Response("Successful Logout", status=status.HTTP_200_OK)
    
    from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated , IsAdminUser

from rest_framework.response import Response

from rest_framework.views import APIView

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password

from rest_framework import status

from .serializers import *

from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)

class GetLoginToken(APIView):
    def post(self, request):
        user = User.objects.filter(username=request.data.get("username")).first()
        password = request.data.get("password")
        role = User.objects.get(username=request.data.get('username'))
        data = role.role

        if user is not None and user.check_password(password):

            refresh = RefreshToken.for_user(user)
            context = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username':str(role.username),
                'role': str(data),
            }
            return Response(context, status.HTTP_200_OK)

            # if user.is_active:
            #     refresh = RefreshToken.for_user(user)
            #     context = {
            #         'refresh': str(refresh),
            #         'access': str(refresh.access_token),
            #     }
            #     return Response(context, status.HTTP_200_OK)
            # else:
            #     context = {
            #         "message": "Please verify your email first!"
            #     }
            #     return Response(context, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            context = {
                "detail": "No active account found with the given credentials"
            }
            return Response(context, status.HTTP_401_UNAUTHORIZED)



