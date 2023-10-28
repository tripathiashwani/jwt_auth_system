from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,loginSerializer,UserProfileSerializer,PasswordChangeSerializer,SendResetPasswordEmailSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            tokens=get_tokens_for_user(user)
            return Response({"msg":"Registration success","tokens":tokens},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=loginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                tokens=get_tokens_for_user(user)
                return Response({'msg':'login success','tokens':tokens},status=status.HTTP_200_OK)
            else :
               return  Response({'erros':{'non_field_errors':['email or password is invalid']}},status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    

class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=PasswordChangeSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
         return Response({"msg":"password changed succesfully "},status=status.HTTP_200_OK)

class SendResetPasswordEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'check your mail for reset link'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
    render_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetView(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password changed successfully'},status=status.HTTP_200_OK)