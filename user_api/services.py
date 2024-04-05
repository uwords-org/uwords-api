from user_api.models import User


class UserService:

    @staticmethod
    def get_users() -> list[User]:
        users = User.objects.filter(is_active=True).all()
        return users

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        try:
            user = User.objects.get(email=email)
            return user
        except:
            return None

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        try:
            user = User.objects.get(id=user_id)
            return user
        except:
            return None
