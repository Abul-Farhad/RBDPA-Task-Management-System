from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
from django.urls import resolve
from accounts.models import CustomUser
from auth.jwt_auth import JWTAuthentication  # Correct import path

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
       
        # List of public route names
        public_routes = ['login', 'register', 'websocket_test']

        # Resolve the current route name
        resolver_match = resolve(request.path)
        route_name = resolver_match.url_name  # Get the name of the route

        # Skip authentication for public routes
        if route_name in public_routes:
            return  # Skip authentication for this request

        # Call the authenticate method directly
        jwt_auth = JWTAuthentication()
        user, _ = jwt_auth.authenticate(request)
        # Attach the user to the request
        request.user = user
        print(f"In middleware, User: {request.user}")