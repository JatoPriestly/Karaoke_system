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

# from rest_framework import serializers
# from .models import User, Song, DuetSession, Performance, FavoriteSongs, DuetHistory

# # User Serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             'id', 'username', 'email', 'display_name', 'profile_picture', 
#             'groups', 'user_permissions'
#         ]
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }

#     def create(self, validated_data):
#         groups_data = validated_data.pop('groups', [])
#         user_permissions_data = validated_data.pop('user_permissions', [])
#         user = User.objects.create_user(**validated_data)
#         user.groups.set(groups_data)
#         user.user_permissions.set(user_permissions_data)
#         return user


#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             if attr == 'password':
#                 instance.set_password(value)
#             else:
#                 setattr(instance, attr, value)
#         instance.save()
#         return instance


# # Song Serializer
# class SongSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Song
#         fields = ['id', 'title', 'artist', 'file_path', 'lyrics_file', 'duration']


# # DuetSession Serializer
# class DuetSessionSerializer(serializers.ModelSerializer):
#     host = serializers.StringRelatedField()
#     participant = serializers.StringRelatedField()

#     class Meta:
#         model = DuetSession
#         fields = [
#             'id', 'host', 'participant', 'song', 
#             'start_time', 'is_active'
#         ]


# # Performance Serializer
# class PerformanceSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()
#     song = serializers.StringRelatedField()

#     class Meta:
#         model = Performance
#         fields = [
#             'id', 'user', 'song', 'timestamp', 
#             'score', 'recording'
#         ]


# # FavoriteSongs Serializer
# class FavoriteSongsSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()
#     song = serializers.StringRelatedField()

#     class Meta:
#         model = FavoriteSongs
#         fields = ['id', 'user', 'song', 'added_on']


# # DuetHistory Serializer
# class DuetHistorySerializer(serializers.ModelSerializer):
#     session = serializers.StringRelatedField()
#     user = serializers.StringRelatedField()

#     class Meta:
#         model = DuetHistory
#         fields = [
#             'id', 'session', 'user', 
#             'recorded_audio', 'performance_score'
#         ]
from rest_framework import serializers
from .models import User, Song, DuetSession, Performance, FavoriteSongs, DuetHistory

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.groups.related.model.objects.all(), required=False
    )
    user_permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.user_permissions.related.model.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'display_name', 
            'profile_picture', 'groups', 'user_permissions'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        user_permissions_data = validated_data.pop('user_permissions', [])
        user = User.objects.create_user(**validated_data)
        user.groups.set(groups_data)
        user.user_permissions.set(user_permissions_data)
        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', [])
        user_permissions_data = validated_data.pop('user_permissions', [])
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        instance.groups.set(groups_data)
        instance.user_permissions.set(user_permissions_data)
        return instance


# Song Serializer
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'file_path', 'lyrics_file', 'duration']


# DuetSession Serializer
class DuetSessionSerializer(serializers.ModelSerializer):
    host = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    participant = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    song = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all())

    class Meta:
        model = DuetSession
        fields = [
            'id', 'host', 'participant', 'song', 
            'start_time', 'is_active'
        ]


# Performance Serializer
class PerformanceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    song = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all())

    class Meta:
        model = Performance
        fields = [
            'id', 'user', 'song', 'timestamp', 
            'score', 'recording'
        ]


# FavoriteSongs Serializer
class FavoriteSongsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    song = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all())

    class Meta:
        model = FavoriteSongs
        fields = ['id', 'user', 'song', 'added_on']


# DuetHistory Serializer
class DuetHistorySerializer(serializers.ModelSerializer):
    session = serializers.PrimaryKeyRelatedField(queryset=DuetSession.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = DuetHistory
        fields = [
            'id', 'session', 'user', 
            'recorded_audio', 'performance_score'
        ]
