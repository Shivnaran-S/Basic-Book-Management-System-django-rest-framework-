from django.shortcuts import render
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import *
from .models import *

class SignupUser(APIView):
    def post(self, request):
        serializedUser = RegisterSerializer(data = request.data)  

        if serializedUser.is_valid():
            user = serializedUser.save()
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            return Response(
                {
                    "data":serializedUser.data,
                    "access_token":access_token,
                    "refresh_token":str(refresh_token)
                },
                
            )
        return Response(serializedUser.errors, status=400)
    
class SigninView(APIView):
    def post(self, request):
        serializedUser = LoginSerializer(data = request.data)
        if serializedUser.is_valid():
            user = AuthModel.objects.get(email = serializedUser.validated_data["email"])
            if not user:
                return Response({"message":"No user with given email id","error":serializedUser.errors})
            
            if not user.checkPassword(serializedUser.validated_data["password"]):
                return Response({"message":"Incorrect Password","error":serializedUser.errors})

            refresh_token = RefreshToken.for_user(user) 
            access_token = str(refresh_token.access_token)
            print(f"Generated Access Token: {access_token}")

            return Response({
                "message":"Signin Success",
                "access_token":access_token,
                "refresh_token":str(refresh_token)
            })
        
class UserDetailsView(APIView):
    authentication_classes = []
    def get(self, request):
        print("Entered UserDetailsView.get")
        auth_header = request.headers.get('Authorization',None)
        if not auth_header:
            raise AuthenticationFailed('Authorization header is expected.')
        
        parts = auth_header.split()
        # Ensure the header is in the expected format
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise AuthenticationFailed('Authorization header must be Bearer token.')

        token = parts[1]
        logging.info("Received token: %s", token)  
        try:
            # Decode and validate the token
            access_token = AccessToken(token)
        except Exception as e:
            raise AuthenticationFailed('Invalid or expired token.')

        # Retrieve the user from the token
        try:
            user_id = access_token['user_id']  # Assuming 'user_id' is part of the token payload
        except KeyError:
            raise AuthenticationFailed('User ID not found in token.')
        
        try:
            user = AuthModel.objects.get(id=user_id)
        except AuthModel.DoesNotExist:
            raise AuthenticationFailed('No user found for this token.')

        # Attach the user to the request (like DRF does with IsAuthenticated)
        request.user = user

        # Now you can safely access the user data in the view
        user_data = {
            "username": user.username,
            "email": user.email,
            "id": user.id,
        }
        return Response(user_data)
