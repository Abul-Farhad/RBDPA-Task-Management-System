from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.urls import resolve
import jwt
from accounts.models import CustomUser

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print("JWTAuthentication.authenticate called")

        auth = request.headers.get('Authorization')
        
        if not auth:
            # raise AuthenticationFailed('Authorization header missing')
            return None

        # Split the 'Authorization' header to extract the token
        parts = auth.split()

        if len(parts) != 2:
            raise AuthenticationFailed('Invalid Authorization header format')
        
        token = parts[1]

        try:
            # Decode the JWT token
            payload = jwt.decode(token, "secret", algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        # Get user from the payload
        try:
            user = CustomUser.objects.get(id=payload['user_id'])
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('User not found')

        # Return the user and None (since we don't need the credentials)
        return (user, None)