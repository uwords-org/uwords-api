from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


from user_api.services import UserService
from user_api.serializers import UserDumpSerializer, UserSerializer, LoginSerializer
from services.response_service import ResponseService


class UserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        users = UserService.get_users()
        return ResponseService.return_success(msg=UserDumpSerializer(users, many=True).data)

    def post(self, request):
        user = UserSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()

        return ResponseService.return_success(msg={"msg": "Пользователь успешно создан"})


class UserLogin(APIView):

    def post(self, request):
        userdata = LoginSerializer(data=request.data)
        userdata.is_valid()

        user = UserService.get_user_by_email(email=userdata.data.get("email", None))

        if not user:
            return ResponseService.return_not_found(msg={"msg": "Пользователь не найден"})

        if userdata.data.get("password", None) == user.password:
            return ResponseService.return_success(msg=UserDumpSerializer(user).data)
        