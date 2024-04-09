import logging
from os import path
import os
import uuid
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from concurrent.futures import ThreadPoolExecutor
from langdetect import detect

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

            with ThreadPoolExecutor(max_workers=20) as executor:
                results_ru = list(executor.map(AudioFileService.speech_to_text_ru, files_paths))
            
            with ThreadPoolExecutor(max_workers=20) as executor:
                results_en = list(executor.map(AudioFileService.speech_to_text_en, files_paths))

            if len(' '.join(results_ru)) > len(' '.join(results_en)):
                is_ru = True
                results = results_ru
            
            else:
                is_ru = False
                results = results_en

            freq_dict = TextService.get_frequency_dict(text=' '.join(results))

            if is_ru:
                translated_words = TextService.translate(words=freq_dict, from_lang="russian", to_lang="english")
            else:
                translated_words = TextService.translate(words=freq_dict, from_lang="english", to_lang="russian")

            UserWordService.upload_user_words(user_words=translated_words, user_id=1)

            user_words = UserWordService.get_user_words(user_id=1)
            
            return ResponseService.return_success(msg={"msg": UserWordSerializer(user_words, many=True).data})

        except Exception as e:
            return ResponseService.return_bad_request(msg={"msg": f"Не удалось загрузить файл. {e}"})
        
        finally:
            for file_path in files_paths + [inp_path, out_path]:
                try:
                    os.remove(path=file_path)
                except:
                    continue
        

class YoutubeAudioAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            youtube = YoutubeAudioSerializer(data=request.data)
            youtube.is_valid(raise_exception=True)

            inp_path, title, video_title = AudioFileService.upload_youtube_audio(link=youtube.data.get("link"))
            out_path = AudioFileService.convert_audio(path=inp_path, title=title)

            files_paths = AudioFileService.cut_audio(path=out_path, title=title)

            lang = detect(video_title)

            if lang == 'ru':
                with ThreadPoolExecutor(max_workers=20) as executor:
                    results = list(executor.map(AudioFileService.speech_to_text_ru, files_paths))
            else:
                with ThreadPoolExecutor(max_workers=20) as executor:
                    results = list(executor.map(AudioFileService.speech_to_text_en, files_paths))

            freq_dict = TextService.get_frequency_dict(text=' '.join(results))

            if lang == 'ru':
                translated_words = TextService.translate(words=freq_dict, from_lang="russian", to_lang="english")
            else:
                translated_words = TextService.translate(words=freq_dict, from_lang="english", to_lang="russian")

            UserWordService.upload_user_words(user_words=translated_words, user_id=1)

            user_words = UserWordService.get_user_words(user_id=1)
            
            return ResponseService.return_success(msg={"msg": UserWordSerializer(user_words, many=True).data})

        except Exception as e:
            return ResponseService.return_bad_request(msg={"msg": f"Не удалось загрузить файл. {e}"})
        
        finally:
            for file_path in files_paths + [inp_path, out_path]:
                try:
                    os.remove(path=file_path)
                except:
                    continue
