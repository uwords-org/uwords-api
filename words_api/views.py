import os
import uuid
import logging
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from user_api.services import UserService
from words_api.services import AudioFileService, UserWordService
from words_api.serializers import UserWordSerializer, YoutubeAudioSerializer

from services.response_service import ResponseService
from words_api.tasks import upload_audio_task, upload_youtube_task


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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


class WordAudioAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            logger.info(f'[AUDIO UPLOAD] Upload started...')
            
            audio_file = request.FILES['file']
            audio_name = request.FILES['file'].name

            _, audio_ext = os.path.splitext(audio_name)

            logger.info(f'[AUDIO] Extension: {audio_ext}')
            
            filename = f'audio_{uuid.uuid4()}{audio_ext}'
            title, ext = os.path.splitext(filename)

            if ext != 'wav':
                inp_path = AudioFileService.upload_audio(audio=audio_file, path=f'input/{filename}')
                out_path = AudioFileService.convert_audio(path=inp_path, title=title)
            else:
                out_path = AudioFileService.upload_audio(audio=audio_file, path=f'output/{filename}')
            
            upload_audio_task.apply_async((out_path, ), countdown=1)
            
            return ResponseService.return_success(msg={"msg": "Загрузка данных началась"})

        except Exception as e:
            return ResponseService.return_bad_request(msg={"msg": f"Не удалось загрузить файл. {e}"})


class YoutubeAudioAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            youtube = YoutubeAudioSerializer(data=request.data)
            youtube.is_valid(raise_exception=True)

            upload_youtube_task.apply_async((youtube.data.get("link", None), ), countdown=1)
            
            return ResponseService.return_success(msg={"msg": "Загрузка видео началась"})

        except Exception as e:
            return ResponseService.return_bad_request(msg={"msg": f"Не удалось загрузить файл. {e}"})
