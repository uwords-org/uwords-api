from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from user_api.services import UserService
from words_api.services import UserWordService
from words_api.serializers import UserWordSerializer

from services.response_service import ResponseService


class UserWordAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id", None)

        if not user_id:
            return ResponseService.return_not_found(msg={"msg": "Пользователь не найден"})

        user = UserService.get_user_by_id(user_id=user_id)

        if not user:
            return ResponseService.return_not_found(msg={"msg": "Пользователь не найден"})

        user_words = UserWordService.get_user_words(user_id=user_id)

        return ResponseService.return_success(msg=UserWordSerializer(user_words, many=True).data)
