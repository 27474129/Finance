from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from website import settings
from user.views import (
    UserRegView, RootView, UserAuthView, UserLogoutView, UserProfileView,
    user, RespectUserProfileAPIView
)
from website.settings import BASE_API_URL


urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/', UserRegView.as_view(), name='reg'),
    path('root/', RootView.as_view(), name='root'),
    path('auth/', UserAuthView.as_view(), name='auth'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user/<int:user_id>/', UserProfileView.as_view(), name='user'),
    path('user/', user, name='base_user'),
]

api_urls = [
    path(f'{BASE_API_URL}respect_user_profile/',
    RespectUserProfileAPIView.as_view(), name='respect_user_profile')
]

urlpatterns += api_urls


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
