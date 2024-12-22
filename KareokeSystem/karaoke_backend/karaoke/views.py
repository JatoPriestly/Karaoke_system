from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Song, DuetSession, FavoriteSongs, Performance
from .serializers import (
    UserSerializer, SongSerializer, DuetSessionSerializer,
    FavoriteSongsSerializer, PerformanceSerializer
)

User = get_user_model()

# User ViewSet
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Song ViewSet
class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]

# DuetSession ViewSet
class DuetSessionViewSet(ModelViewSet):
    queryset = DuetSession.objects.all()
    serializer_class = DuetSessionSerializer
    permission_classes = [IsAuthenticated]

# FavoriteSongs ViewSet
class FavoriteSongsViewSet(ModelViewSet):
    queryset = FavoriteSongs.objects.all()
    serializer_class = FavoriteSongsSerializer
    permission_classes = [IsAuthenticated]

# Performance ViewSet
class PerformanceViewSet(ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated]

# External API Search View
class ExternalAPISearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Example placeholder implementation
        return Response({"message": "Search external APIs here."}, status=status.HTTP_200_OK)

# External API Sync View
class ExternalAPISyncView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Example placeholder implementation
        return Response({"message": "Sync external APIs here."}, status=status.HTTP_200_OK)

# Lyrics View
class LyricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # Example placeholder implementation
        return Response({"lyrics": f"Lyrics for song with id {id}."}, status=status.HTTP_200_OK)

# Real-Time Duet View
class RealTimeDuetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # Example placeholder implementation
        return Response({"message": f"Real-time duet for session {id}."}, status=status.HTTP_200_OK)

# Status View
class StatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "Server is running."}, status=status.HTTP_200_OK)

# Register User View
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

# Logout View
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

# User Profile View
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
