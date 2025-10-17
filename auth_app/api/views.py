from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer, LoginSerializer, CheckUserEmial
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status



class RegistrationView(APIView):
    permission_classes = [AllowAny]
    data = {}

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        

        if serializer.is_valid():
            user =  serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            data = {
                    "token": token.key,
                    "fullname": user.username,
                    "email": user.email,
                    "user_id": user.id
                }
        else:
            data = serializer.errors
        return Response(data)
    
class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    data = {}

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                    "token": token.key,
                    "fullname": user.username,
                    "email": user.email,
                    "user_id": user.id
                }
        else:
            data = serializer.errors

        return Response(data)
    
class UserEmailCheck(APIView):


    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email')
        serializer = CheckUserEmial(data={'email':email})

        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            data = {
                'id': user.id,
                'email': user.email,
                'fullname': user.username
            }

            return Response(data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        
        
        