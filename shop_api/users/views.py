from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Code
from django.utils import timezone
from random import randint
from django.core.mail import send_mail
from .serializers import UserRegistrationValidationSerializer,UserAuthenticationValidationSerializer,CodeValidationSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
# Create your views here.

class RegisterView(CreateAPIView):
    serializer_class = UserRegistrationValidationSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data['email']
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_active=False
        )
        code = int(('').join([str(randint(0, 9)) for i in range(6)]))
        deadline = timezone.now() + timezone.timedelta(minutes=4)
        Code.objects.create(user=user, code=code, deadline=deadline)
        return Response(data={'code': code}, status=status.HTTP_201_CREATED)


class LoginView(CreateAPIView):
    serializer_class = UserAuthenticationValidationSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(data={'error': 'user does not exist'}, status=status.HTTP_401_UNAUTHORIZED)

class CodeView(CreateAPIView):
    serializer_class = CodeValidationSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']
        try:
            user_code = Code.objects.get(code=code)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user_code.deadline <= timezone.now():
            user_code.delete()
            code = int(('').join([str(randint(0, 9)) for i in range(6)]))
            deadline = timezone.now() + timezone.timedelta(minutes=4)
            Code.objects.create(user=user_code.user, code=code, deadline=deadline)
            return Response(data={'error': code}, status=status.HTTP_404_NOT_FOUND)

        user_code.user.is_active = True
        user_code.user.save()
        user_code.delete()
        return Response(data={'active': True}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def register_api_view(request):
#     serializer = UserRegistrationValidationSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     username = serializer.validated_data['username']
#     password = serializer.validated_data['password']
#     email = serializer.validated_data['email']
#     user = User.objects.create_user(
#         username=username,
#         password=password,
#         email=email,
#         is_active=False
#     )
#     code=int(('').join([str(randint(0, 9)) for i in range(6)]))
#     deadline=timezone.now()+timezone.timedelta(minutes=4)
#     Code.objects.create(user=user,code=code,deadline=deadline)
#     send_mail('Hi',
#               f'your code: {code}\ncode expires in 4 min',
#               EMAIL_HOST_USER,
#               recipient_list=[user.email])
#     return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# def authentication_api_view(request):
#     serializer = UserAuthenticationValidationSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     user=authenticate(**serializer.validated_data)
#     if user:
#         token,created=Token.objects.get_or_create(user=user)
#         return Response(data={'key':token.key})
#     return Response(data={'error':'user does not exist'}, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# def confirm_api_view(request):
#     serializer = CodeValidationSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     code=serializer.validated_data['code']
#     try:
#         user_code=Code.objects.get(code=code)
#     except Exception as e:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if user_code.deadline <= timezone.now():
#         user_code.delete()
#         code = int(('').join([str(randint(0, 9)) for i in range(6)]))
#         deadline = timezone.now() + timezone.timedelta(minutes=4)
#         Code.objects.create(user=user_code.user, code=code, deadline=deadline)
#         send_mail('Expired',
#                   f'your new code: {code}\ncode expires in 4 min',
#                   EMAIL_HOST_USER,
#                   recipient_list=[user_code.user.email])
#         return Response(data={'error':'code expired'}, status=status.HTTP_404_NOT_FOUND)
#
#     user_code.user.is_active = True
#     user_code.user.save()
#     user_code.delete()
#     return Response(data={'active':True}, status=status.HTTP_200_OK)