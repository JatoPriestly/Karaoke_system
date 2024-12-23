from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Song, DuetSession, FavoriteSongs, Performance

User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture']
        read_only_fields = ['id']

# Song Serializer
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'duration', 'file_path', 'uploaded_by', 'created_at']
        read_only_fields = ['id', 'uploaded_by', 'created_at']

# DuetSession Serializer
class DuetSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuetSession
        fields = ['id', 'song', 'participants', 'start_time', 'end_time', 'is_active']
        read_only_fields = ['id', 'start_time', 'end_time']

# FavoriteSongs Serializer
class FavoriteSongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteSongs
        fields = ['id', 'user', 'song', 'added_at']
        read_only_fields = ['id', 'added_at']

# Performance Serializer
class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ['id', 'user', 'song', 'score', 'performance_file', 'created_at']
        read_only_fields = ['id', 'created_at']
