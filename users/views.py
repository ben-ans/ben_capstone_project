from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .authentication import CustomTokenAuthentication


from .serializers import UserSerializer, AuthTokenSerializer

class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer

class UserRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user




class CustomObtainAuthTokenView(ObtainAuthToken):
    serializer_class= AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            token = response.data.get('token')

            response.set_cookie(
                settings.AUTH_COOKIE,
                token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE

            )

            return response




class LogoutView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Delete the DRF token object
        request.auth.delete()

        # Clear the cookie
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie(settings.AUTH_COOKIE)
        return response

