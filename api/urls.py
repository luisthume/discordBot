from django.urls import path, include

from .views import (
    DiscordUsers,
    DiscordUser,
    HoursAPIView,
    HourAPIView,
    HourByCodeAPIView,
    HitMinuteAPIView,
    HitMinuteByCodeAPIView
)

urlpatterns = [
    path('users/', DiscordUsers.as_view()),
    path('users/<int:pk>/', DiscordUser.as_view()),

    path('hours/', HoursAPIView.as_view()),
    path('hours/<int:pk>/', HourAPIView.as_view(), name='hour'),
    path('hours/code/<str:code>/', HourByCodeAPIView.as_view(), name='hour_code'),

    path('minutes/<int:pk>', HitMinuteAPIView.as_view()),
    path('minutes/code/<str:code>', HitMinuteByCodeAPIView.as_view())
]