from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import validate_email


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users with email, password, and repeated password.
    """

    repeated_password = serializers.CharField(write_only = True)
    fullname = serializers.CharField(source= 'username')

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_email(self, value):
        """
        Ensures the email address is unique across users.
        """
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    def validate_fullname(self, value):
        """
        Ensures the username (fullname) is unique across users.
        """
        if User.objects.filter(username = value).exists():
            raise serializers.ValidationError('Username already exists')
        return value
    
    def validate(self, attrs):

        allowed_fields = set(self.fields.keys())
        incomming_fields = set(self.initial_data.keys())

        extra_fields = incomming_fields - allowed_fields
        if extra_fields:
            raise serializers.ValidationError({k: "Unerwartetes Feld." for k in extra_fields})
        return attrs
    

    

    def save(self, **kwargs):
        """
        Creates a new user after verifying that both password fields match.
        """
        pw = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']

        if pw != repeated_password:
            raise serializers.ValidationError({'error': 'Passwords don\'t match'})
        
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account
    

class LoginSerializer(serializers.Serializer):
    """
    Serializer for authenticating a user using email and password.
    """
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        """
        Authenticates the user and attaches the user instance to attrs['user'].
        """
        email = attrs.get('email')
        password = attrs.get('password')
        is_a_user = User.objects.filter(email=email).exists()
        username = None

        if is_a_user:
            username = User.objects.get(email=email).username
        else:
             msg = 'Email address is not found'
             raise serializers.ValidationError(msg, code='authorization')

        if email and password and username:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    
class UserSerializer(serializers.ModelSerializer):
    """
    Read-only user representation exposing id, fullname, and email.
    """
    fullname = serializers.CharField(source= 'username')
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email']


class CheckUserEmial(serializers.Serializer):
    """
    Serializer for validating an email and resolving it to an existing user.
    """
    email= serializers.EmailField()

    def validate(self, attrs):
        """
        Validates the email format and existence, then attaches the user to attrs['user'].
        """
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()

        if not email:
            msg = "This field is required"
            raise serializers.ValidationError(msg, code="unvalid_email_adresse")
        
        try:
            validate_email(email)
        except:
            msg = "Enter a valid email"
            raise serializers.ValidationError(msg, code="unvalid_email")
        
        if not user:
            msg = "This user is not a member"
            raise serializers.ValidationError(msg, code="unvalid_email")
        
        attrs['user'] = user
        return attrs
        









