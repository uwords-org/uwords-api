from words_api.models import UserWord


class UserWordService:

    @staticmethod
    def get_user_words(user_id: int) -> list[UserWord]:
        user_words = UserWord.objects.filter(user__id=user_id).all()
        return user_words

