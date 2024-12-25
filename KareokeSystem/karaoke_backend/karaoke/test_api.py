from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from karaoke.models import (
    User, Song, DuetSession, Performance, FavoriteSongs, DuetHistory
)
from karaoke.serializers import (
    UserSerializer, SongSerializer, DuetSessionSerializer,
    PerformanceSerializer, FavoriteSongsSerializer, DuetHistorySerializer
)
from django.contrib.auth.models import Group, Permission

class SerializerTestCase(APITestCase):
    def setUp(self):
        # Create sample data for testing
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
            display_name="Test User"
        )
        self.song = Song.objects.create(
            title="Test Song",
            artist="Test Artist",
            file_path="songs/test_song.mp3",
            lyrics_file="lyrics/test_song.lrc",
            duration=240
        )
        self.group = Group.objects.create(name="Test Group")
        self.permission = Permission.objects.first()

    # Test UserSerializer
    def test_user_serializer(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "display_name": "New User",
            "groups": [{"id": self.group.id}],
            "user_permissions": [{"id": self.permission.id}],
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.groups.first().id, self.group.id)

    # Test SongSerializer
    def test_song_serializer(self):
        data = {
            "title": "New Song",
            "artist": "New Artist",
            "file_path": "songs/new_song.mp3",
            "lyrics_file": "lyrics/new_song.lrc",
            "duration": 300,
        }
        serializer = SongSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        song = serializer.save()
        self.assertEqual(song.title, data["title"])
        self.assertEqual(song.artist, data["artist"])

    # Test DuetSessionSerializer
    def test_duet_session_serializer(self):
        data = {
            "host": self.user.id,
            "participant": None,
            "song": self.song.id,
            "start_time": "2024-12-25T12:00:00Z",
            "is_active": True,
        }
        serializer = DuetSessionSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        duet_session = serializer.save()
        self.assertEqual(duet_session.host.id, self.user.id)
        self.assertEqual(duet_session.song.id, self.song.id)

    # Test PerformanceSerializer
    def test_performance_serializer(self):
        data = {
            "user": self.user.id,
            "song": self.song.id,
            "timestamp": "2024-12-25T12:00:00Z",
            "score": 95,
            "recording": None,
        }
        serializer = PerformanceSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        performance = serializer.save()
        self.assertEqual(performance.user.id, self.user.id)
        self.assertEqual(performance.song.id, self.song.id)

    # Test FavoriteSongsSerializer
    def test_favorite_songs_serializer(self):
        data = {
            "user": self.user.id,
            "song": self.song.id,
            "added_on": "2024-12-25T12:00:00Z",
        }
        serializer = FavoriteSongsSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        favorite_song = serializer.save()
        self.assertEqual(favorite_song.user.id, self.user.id)
        self.assertEqual(favorite_song.song.id, self.song.id)

    # Test DuetHistorySerializer
    def test_duet_history_serializer(self):
        duet_session = DuetSession.objects.create(
            host=self.user,
            participant=None,
            song=self.song,
            start_time="2024-12-25T12:00:00Z",
            is_active=False,
        )
        data = {
            "session": duet_session.id,
            "user": self.user.id,
            "recorded_audio": "recordings/duet_audio.mp3",
            "performance_score": 88,
        }
        serializer = DuetHistorySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        duet_history = serializer.save()
        self.assertEqual(duet_history.session.id, duet_session.id)
        self.assertEqual(duet_history.user.id, self.user.id)

    # Test Validation Errors
    def test_invalid_user_serializer(self):
        data = {"username": "", "email": "invalid", "password": ""}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
        self.assertIn("email", serializer.errors)
        self.assertIn("password", serializer.errors)

