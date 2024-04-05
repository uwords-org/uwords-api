from django.urls import path

from words_api.views import (
    UserWordAPIView,
    WordAudioAPIView,
    YoutubeAudioAPIView
)

urlpatterns = [
    path('user/<int:user_id>', UserWordAPIView.as_view()),
    path('audio', WordAudioAPIView.as_view()),
    path('youtube', YoutubeAudioAPIView.as_view()),
]
