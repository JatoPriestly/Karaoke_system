from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import User, Song, DuetSession, FavoriteSongs, Performance
from .serializers import (
    UserSerializer,
    SongSerializer,
    DuetSessionSerializer,
    FavoriteSongsSerializer,
    PerformanceSerializer
)
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsOwnerOrReadOnly

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

# Song ViewSet
class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

# DuetSession ViewSet
class DuetSessionViewSet(viewsets.ModelViewSet):
    queryset = DuetSession.objects.all()
    serializer_class = DuetSessionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

# FavoriteSongs ViewSet
class FavoriteSongsViewSet(viewsets.ModelViewSet):
    queryset = FavoriteSongs.objects.all()
    serializer_class = FavoriteSongsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Performance ViewSet
class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Register User View
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logout View
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# User Profile View
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# External API Search View
class ExternalAPISearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Example placeholder logic for external API search
        query = request.query_params.get("q", "")
        if query:
            return Response({"results": [f"Found {query}."]})
        return Response({"results": []})

# External API Sync View
class ExternalAPISyncView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Example placeholder logic for syncing
        return Response({"detail": "External data synced successfully."})

# Lyrics View
class LyricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        song = get_object_or_404(Song, id=id)
        return Response({"lyrics": f"Lyrics for {song.title} by {song.artist}."})

# Real-Time Duet View
class RealTimeDuetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        session = get_object_or_404(DuetSession, id=id)
        if session.is_active:
            return Response({"detail": "Duet session is active.", "participants": session.participants.values_list("username", flat=True)})
        return Response({"detail": "Duet session is not active."})

# Status View
class StatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "API is running smoothly."})
