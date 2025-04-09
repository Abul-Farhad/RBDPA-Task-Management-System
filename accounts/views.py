from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
import jwt,datetime
import os

User = get_user_model()

class RegisterUserView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required!"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists!"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, password=password)
        return Response({"message": "User created successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)

class LoginUserView(APIView):   
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response({"error": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)
            
            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            secret_key = os.getenv('JWT_SECRET_KEY')
            token = jwt.encode(payload, secret_key, algorithm='HS256')
            response = Response()
            response.data = {
                'message': 'Login successful!',
                'token': token
            }
            response.status_code = 200
            return response
            
        except User.DoesNotExist:
            return Response({"error": "User does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    