from django.contrib import admin
from .models import User, Song, DuetSession, FavoriteSongs, DuetHistory

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'display_name')
    search_fields = ('username', 'email', 'display_name')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'duration')
    search_fields = ('title', 'artist')
    list_filter = ('artist',)

@admin.register(DuetSession)
class DuetSessionAdmin(admin.ModelAdmin):
    list_display = ('host', 'participant', 'song', 'is_active', 'start_time')
    list_filter = ('is_active', 'start_time')
