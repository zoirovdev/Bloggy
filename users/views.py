from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer

from .serializers import UserSerializer, LoginSerializer
from .models import User

from drf_spectacular.utils import extend_schema

class UserList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=UserSerializer)
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=
            { 
            'application/json': UserSerializer, 
            'multipart/form-data': UserSerializer  
            },
        responses=UserSerializer
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = serializer.instance
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=
            { 
            'application/json': LoginSerializer, 
            'multipart/form-data': LoginSerializer  
            },
        responses=UserSerializer
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=UserSerializer)
    def get(self, request, pk=None):
        if pk:
            user = User.objects.get(pk=pk)
        else:
            user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutAPIView(APIView):
    @extend_schema(responses=UserSerializer)
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a RefreshToken object
            token = RefreshToken(refresh_token)

            # Blacklist the token
            token.blacklist()

            return Response({'detail': 'Logout successful.'}, status=status.HTTP_205_RESET_CONTENT)

        except (TokenError, InvalidToken) as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)



