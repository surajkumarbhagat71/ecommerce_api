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
    
    
