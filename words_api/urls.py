from django.urls import path

from words_api.views import (
    UserWordAPIView
)

urlpatterns = [
    path('user/<int:user_id>', UserWordAPIView.as_view())
]
