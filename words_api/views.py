import logging
from os import path
import os
import uuid
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from user_api.services import UserService
from words_api.services import AudioFileService, TextService, UserWordService
from words_api.serializers import UserWordSerializer, YoutubeAudioSerializer

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


class WordAudioAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            audio_file = request.FILES['file']
            audio_name = request.FILES['file'].name
            
            _, audio_ext = path.splitext(audio_name)
            
            filename = f'audio_{uuid.uuid4()}.{audio_ext}'

            title, ext = path.splitext(filename)

            if ext != 'wav':
                inp_path = AudioFileService.upload_audio(audio=audio_file, path=f'input/{filename}')
                out_path = AudioFileService.convert_audio(path=inp_path, title=title)
            else:
                out_path = AudioFileService.upload_audio(audio=audio_file, path=f'output/{filename}')

            files_paths = AudioFileService.cut_audio(path=out_path, title=title)

            result = []

            for file_path in files_paths:
                text = AudioFileService.speech_to_text(filepath=file_path)
                result.append(text)

                os.remove(path=file_path)

            os.remove(path=inp_path)
            os.remove(path=out_path)

            freq_dict = TextService.get_frequency_dict(text=' '.join(result))

            return ResponseService.return_success(msg={"msg": freq_dict})

        except Exception as e:
            return ResponseService.return_bad_request(msg={"msg": f"Не удалось загрузить файл. {e}"})
        

class YoutubeAudioAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            youtube = YoutubeAudioSerializer(data=request.data)
            youtube.is_valid(raise_exception=True)

            inp_path, title = AudioFileService.upload_youtube_audio(link=youtube.data.get("link"))
            out_path = AudioFileService.convert_audio(path=inp_path, title=title)

            files_paths = AudioFileService.cut_audio(path=out_path, title=title)

            result = []

            for file_path in files_paths:
                text = AudioFileService.speech_to_text(filepath=file_path)
                result.append(text)
                
                os.remove(path=file_path)

            os.remove(path=inp_path)
            os.remove(path=out_path)

            freq_dict = TextService.get_frequency_dict(text=' '.join(result))

            return ResponseService.return_success(msg={"msg": freq_dict})

        except Exception as e:
            return ResponseService.return_bad_request(msg={"msg": f"Не удалось загрузить файл. {e}"})
