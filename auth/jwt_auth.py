from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model  

User = get_user_model()

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization')
        
        if not auth:
            raise AuthenticationFailed('Authorization header missing')

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
        user = User.objects.get(id=payload['user_id'])

        # Return the user and None (since we don't need the credentials)
        return (user, None)
