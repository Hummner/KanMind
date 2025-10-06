from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User



class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully.'})
        return Response(serializer.errors)
    
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


        
