from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
from django.urls import resolve
from accounts.models import CustomUser
from auth.jwt_auth import JWTAuthentication


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip middleware for admin, static, or media URLs
        if (
            request.path.startswith('/admin') or
            request.path.startswith('/static') or
            request.path.startswith('/media')
        ):
            return

        # List of public route names (urls with no JWT required)
        public_routes = ['login', 'register', 'websocket_test']

        try:
            resolver_match = resolve(request.path)
            route_name = resolver_match.url_name
        except:
            # Some admin/static paths might not resolve properly, skip them
            return

        if route_name in public_routes:
            return  # Allow public access

        # Authenticate request
        jwt_auth = JWTAuthentication()
        result = jwt_auth.authenticate(request)

        if result is None:
            raise AuthenticationFailed('Authentication credentials were not provided.')

        request.user, _ = result
