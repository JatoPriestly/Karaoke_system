from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet,
    SongViewSet,
    DuetSessionViewSet,
    FavoriteSongsViewSet,
    PerformanceViewSet,
    ExternalAPISearchView,
    ExternalAPISyncView,
    LyricsView,
    RealTimeDuetView,
    StatusView,
    RegisterUserView,
    LogoutView,
    UserProfileView,
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'songs', SongViewSet, basename='song')
router.register(r'duets', DuetSessionViewSet, basename='duet')
router.register(r'favorites', FavoriteSongsViewSet, basename='favorite')
router.register(r'performance', PerformanceViewSet, basename='performance')

# Define additional endpoints
urlpatterns = [
    # Include router-generated URLs
    path('', include(router.urls)),

    # Authentication endpoints
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    # User profile management
    path('users/<int:id>/profile/', UserProfileView.as_view(), name='user_profile'),

    # External API integration
    path('external/search/', ExternalAPISearchView.as_view(), name='external_search'),
    path('external/sync/', ExternalAPISyncView.as_view(), name='external_sync'),

    # Real-time and utility endpoints
    path('lyrics/<int:id>/', LyricsView.as_view(), name='lyrics'),
    path('realtime/duets/<int:id>/', RealTimeDuetView.as_view(), name='realtime_duet'),
    path('status/', StatusView.as_view(), name='status'),
]
