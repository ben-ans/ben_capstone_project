from django.conf import settings

from rest_framework.authentication import TokenAuthentication

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Read the token from cookie
        token = request.COOKIES.get(settings.AUTH_COOKIE)

        if not token:
            return None
        # Validate the token string and return (user, token)
        return self.authenticate_credentials(token)
    
