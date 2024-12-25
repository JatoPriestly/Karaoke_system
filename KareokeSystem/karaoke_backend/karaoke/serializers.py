# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from .models import User
# from .models import Song, DuetSession, FavoriteSongs, Performance

# User = get_user_model()

# # User Serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture']
#         read_only_fields = ['id']

# # Song Serializer
# class SongSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Song
#         fields = ['id', 'title', 'artist', 'duration', 'file_path', 'uploaded_by', 'created_at']
#         read_only_fields = ['id', 'uploaded_by', 'created_at']

# # DuetSession Serializer
# class DuetSessionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DuetSession
#         fields = ['id', 'song', 'participants', 'start_time', 'end_time', 'is_active']
#         read_only_fields = ['id', 'start_time', 'end_time']

# # FavoriteSongs Serializer
# class FavoriteSongsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FavoriteSongs
#         fields = ['id', 'user', 'song', 'added_at']
#         read_only_fields = ['id', 'added_at']

# # Performance Serializer
# class PerformanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Performance
#         fields = ['id', 'user', 'song', 'score', 'performance_file', 'created_at']
#         read_only_fields = ['id', 'created_at']

from rest_framework import serializers
from .models import User, Song, DuetSession, Performance, FavoriteSongs, DuetHistory

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'display_name', 'profile_picture', 
            'groups', 'user_permissions'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


# Song Serializer
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'file_path', 'lyrics_file', 'duration']


# DuetSession Serializer
class DuetSessionSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField()
    participant = serializers.StringRelatedField()

    class Meta:
        model = DuetSession
        fields = [
            'id', 'host', 'participant', 'song', 
            'start_time', 'is_active'
        ]


# Performance Serializer
class PerformanceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    song = serializers.StringRelatedField()

    class Meta:
        model = Performance
        fields = [
            'id', 'user', 'song', 'timestamp', 
            'score', 'recording'
        ]


# FavoriteSongs Serializer
class FavoriteSongsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    song = serializers.StringRelatedField()

    class Meta:
        model = FavoriteSongs
        fields = ['id', 'user', 'song', 'added_on']


# DuetHistory Serializer
class DuetHistorySerializer(serializers.ModelSerializer):
    session = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = DuetHistory
        fields = [
            'id', 'session', 'user', 
            'recorded_audio', 'performance_score'
        ]
