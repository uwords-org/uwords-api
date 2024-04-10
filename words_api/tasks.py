import os
import uuid
import logging
from typing import Any
from langdetect import detect
from uwords_api.celery_app import app
from concurrent.futures import ThreadPoolExecutor
from celery.exceptions import MaxRetriesExceededError


from words_api.services import AudioFileService, TextService, UserWordService


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.task(bind=True, max_retries=2)
def upload_audio_task(self, out_path: str):
    try:
        result = upload_audio(out_path=out_path)

        if not result:
            raise self.retry(countdown=1)

        return 'Загрузка аудио окончена'
    
    except MaxRetriesExceededError:
        return 'Возникла ошибка загрузки аудио'
    

@app.task(bind=True, max_retries=2)
def upload_youtube_task(self, link: str):
    try:
        result = upload_youtube(link=link)

        if not result:
            raise self.retry(countdown=1)
        
        return 'Загрузка видео окончена'
    
    except MaxRetriesExceededError:
        return 'Возникла ошибка загрузки видео'
    
def upload_audio(out_path: str):
    try:

        logger.info(f'[AUDIO UPLOAD] {out_path}')
        
        files_paths = AudioFileService.cut_audio(path=out_path)

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

        logger.info(f'[AUDIO UPLOAD] Upload ended successfully!')

        return True

    except Exception as e:
        logger.info(f'[AUDIO UPLOAD] Error occured!')
        logger.info(e)
        return False
        
    finally:
        for file_path in files_paths + [out_path]:
            try:
                os.remove(path=file_path)
            except:
                continue


def upload_youtube(link: str):
    try:
        logger.info(f'[YOUTUBE UPLOAD] Upload started...')

        inp_path, title, video_title = AudioFileService.upload_youtube_audio(link=link)
        out_path = AudioFileService.convert_audio(path=inp_path, title=title)

        files_paths = AudioFileService.cut_audio(path=out_path)

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

        logger.info(f'[YOUTUBE UPLOAD] Upload ended successfully!')

        return True

    except Exception as e:
        logger.info(f'[YOUTUBE UPLOAD] Error occured')
        logger.info(e)
        return False
        
    finally:
        for file_path in files_paths + [inp_path, out_path]:
            try:
                os.remove(path=file_path)
            except:
                continue