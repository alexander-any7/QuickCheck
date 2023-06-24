from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from accounts.tokens import create_jwt_pair_for_user
from accounts.serializers import UserRegisterSerializer, LoginSerializer


class RegisterUser(APIView):
    '''Handle user registration'''

    def post(self, request):
        # Handle the POST request for user registration
        data = request.data
        if request.user.is_authenticated:
            # If the user is already authenticated, return an error response
            return Response({"message":"User is authenticated"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserRegisterSerializer(data=data)

        if serializer.is_valid():
            # If the serializer data is valid, save the user and return a success response
            serializer.save()
            response = {
                "message" : "User created successfully",
                "data" : serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        # If the serializer data is invalid, return an error response with the validation errors
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginUser(APIView):
    '''Handle user login'''

    serializer_class = LoginSerializer

    def post(self, request):
        # Handle the POST request for user login
        if request.user.is_authenticated:
            # If the user is already authenticated, return an error response
            return Response({"message":"User is authenticated"}, status=status.HTTP_400_BAD_REQUEST) 
        
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # If the user is authenticated, generate JWT pair and return a success response
            tokens = create_jwt_pair_for_user(user)
            response = {
                "message" : "Login Successful",
                "token" : tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            # If the user is not authenticated, return an error response
            return Response({"message" : "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        # Handle the GET request to retrieve user information
        content =  {
            "user" : str(request.user)
        }
        return Response(data=content, status=status.HTTP_200_OK)