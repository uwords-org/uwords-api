import os
import json
import uuid
import string
import logging
import pymorphy3
import subprocess
from gtts import gTTS
from io import BytesIO
from minio import Minio
from pytube import YouTube
from typing import BinaryIO
from librosa import get_duration
from googletrans import Translator
from speech_recognition import Recognizer, AudioFile

from user_api.services import UserService
from words_api.models import UserWord, Word
from uwords_api.instance import (
    STOPWORDS, 
    MINIO_ENDPOINT, 
    MINIO_ROOT_USER, 
    MINIO_ROOT_PASSWORD,
    MINIO_BUCKET_VOICEOVER
)


sr = Recognizer()

mc = Minio(
    MINIO_ENDPOINT, 
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD, 
    secure=False
)


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AudioFileService:

    @staticmethod
    def upload_audio(audio: any, path: str) -> str:
        try:
            destination = open(path, "wb")
            
            for chunk in audio.chunks():
                destination.write(chunk)

            return path
        
        except Exception as e:
            logger.info(e)
            return None
        
    @staticmethod
    def upload_youtube_audio(link: str):
        try:
            video = YouTube(link)

            stream = video.streams.filter(only_audio=True).first()

            filename = f'audio_{uuid.uuid4()}'

            download_path = f"input/{filename}.mp3"

            stream.download(filename=download_path)

            return download_path, filename, video.title
        except Exception as e:
            logger.info(e)
            return None
    
    @staticmethod
    def cut_audio(path: str) -> list[str]:
        files = []
        
        try:
            index = 0
            duration = get_duration(filename=path)
            
            while index * 30 < duration:
                new_path, audio_ext = os.path.splitext(path)

                logger.info(f'[AUDIO] path: {path} new_path: {new_path}_{index + 1}.wav')

                if (index + 1) * 30 < duration:
                    cmd = f'ffmpeg -ss {index * 30} -i {path} -t 30 -ac 1 {new_path}_{index + 1}.wav -y'
                else:
                    cmd = f'ffmpeg -ss {index * 30} -i {path} -ac 1 {new_path}_{index + 1}.wav -y'

                subprocess.call(cmd, shell=True)
                
                files.append(f'{new_path}_{index + 1}.wav')
                index += 1

            return files
        
        except Exception as e:
            logger.info(e)
            return None

    @staticmethod
    def convert_audio(path: str, title: str) -> str:
        try:
            out_path = f'output/{title}.wav'
            cmd = f'ffmpeg -i {path} -ac 1 {out_path} -y'
            
            subprocess.call(cmd, shell=True)
            
            return out_path
        
        except Exception as e:
            logger.info(e)
            return None
        
    @staticmethod
    def speech_to_text_en(filepath: str) -> str:
        try:
            with AudioFile(filepath) as source:
                audio_data = sr.record(source)
                text = sr.recognize_google(audio_data, language='en-US')
      
                return text.lower()
        
        except Exception as e:
            logger.info(e)
            return ' '
        
    @staticmethod
    def speech_to_text_ru(filepath: str) -> str:
        try:
            with AudioFile(filepath) as source:
                audio_data = sr.record(source)
                text = sr.recognize_google(audio_data, language='ru-RU')

                return text.lower()
        
        except Exception as e:
            logger.info(e)
            return ' '
        
    @staticmethod
    def word_to_speech(word: str):
        try:
            tts = gTTS(text=word, lang='en', slow=False)
            
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            object_name = f'{"_".join(word.lower().split())}.mp3'

            MinioUploader.upload_object(
                bucket_name=MINIO_BUCKET_VOICEOVER,
                object_name=object_name,
                data=fp,
                lenght=fp.getbuffer().nbytes
            )
            
            return object_name
        
        except Exception as e:
            logger.info(e)
            return None

    @staticmethod
    def detect_lang(filepath: str) -> str:
        try:
            with AudioFile(filepath) as source:
                audio_data = sr.record(source)
                
                text_ru = sr.recognize_google(audio_data, language='ru-RU')
                text_en = sr.recognize_google(audio_data, language='en-US')

                if len(text_ru) > len(text_en):
                    return True
                
                return False
        
        except Exception as e:
            logger.info(e)
            return False
        

class TextService:

    @staticmethod
    def remove_spec_chars(text: str) -> str:
        spec_chars = string.punctuation + '\n\xa0«»\t—…' + '0123456789'
        return "".join([char for char in text if char not in spec_chars])
    
    @staticmethod
    def remove_stop_words(text: str) -> list[str]:
        return [word for word in text.split() if word not in STOPWORDS]
    
    @staticmethod
    def normalize_words(words: list[str]) -> list[str]:
        norm_words = []
        
        for word in words:
            norm_words.append(pymorphy3.analyzer.MorphAnalyzer().parse(word)[0].normal_form)

        return norm_words
    
    @staticmethod
    def create_freq_dict(words: list[str]) -> dict:
        freq_dict = {}
        
        for word in words:
            if word not in freq_dict.keys():
                freq_dict[word] = 1
            else:
                freq_dict[word] += 1

        return dict(sorted(freq_dict.items(), key=lambda x: x[1], reverse=True))
    
    @staticmethod
    def get_frequency_dict(text: str) -> dict:
        text_without_spec_chars = TextService.remove_spec_chars(text=text)
        
        words = TextService.remove_stop_words(text=text_without_spec_chars)

        norm_words = TextService.normalize_words(words=words)

        freq_dict = TextService.create_freq_dict(words=norm_words)
        
        return freq_dict
    
    @staticmethod
    def translate(words: dict, from_lang: str, to_lang: str) -> list[dict]:
        translator = Translator()

        translated_words = []

        for word in words.keys():
            try:
                translated = translator.translate(word, src=from_lang, dest=to_lang)

                if from_lang == "russian":
                    translated_words.append({
                        'ruValue': word.capitalize(),
                        'enValue': translated.text.capitalize(),
                        'frequency': words[word]
                    })
                
                else:
                    translated_words.append({
                        'ruValue': translated.text.capitalize(),
                        'enValue': word.capitalize(),
                        'frequency': words[word]
                    })

            except Exception as e:
                logger.info(e)
                continue

        return translated_words


class WordService:

    @staticmethod
    def get_word(enValue: str) -> Word:
        try:
            word = Word.objects.get(enValue=enValue)
            return word
        
        except:
            return None

    @staticmethod
    def upload_new_word(enValue: str, ruValue: str) -> Word:
        audioLink = AudioFileService.word_to_speech(word=enValue)
        new_word = Word.objects.create(enValue=enValue, ruValue=ruValue, audioLink=audioLink)
        
        return new_word


class UserWordService:

    @staticmethod
    def get_user_words(user_id: int) -> list[UserWord]:
        user_words = UserWord.objects.filter(user__id=user_id).all().order_by('-frequency')
        return user_words
    
    @staticmethod
    def get_user_word(user_id: int, word_id: int) -> UserWord:
        try:
            user_word = UserWord.objects.get(user__id=user_id, word__id=word_id)
            return user_word
        except:
            return None
    
    @staticmethod
    def upload_user_words(user_words: list[dict], user_id: int) -> bool:

        user = UserService.get_user_by_id(user_id=user_id)

        for user_word in user_words:
            enValue = user_word.get('enValue', None)
            ruValue = user_word.get('ruValue', None)
            frequency = user_word.get('frequency', None)

            word = WordService.get_word(enValue=enValue)

            if not word:
                word = WordService.upload_new_word(enValue=enValue, ruValue=ruValue)

            user_word = UserWordService.get_user_word(user_id=user_id, word_id=word.id)

            if not user_word:
                user_word = UserWord.objects.create(word=word, user=user, frequency=frequency)

            else:
                user_word.frequency += frequency
                user_word.save()

        return True


class MinioUploader:

    @staticmethod
    def upload_object(bucket_name: str, object_name: str, data: BinaryIO, lenght: int):
        try:
            found = mc.bucket_exists(bucket_name)

            if not found:
                policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": "*"},
                            "Action": [
                                "s3:GetBucketLocation",
                                "s3:ListBucket",
                                "s3:ListBucketMultipartUploads",
                            ],
                            "Resource": f"arn:aws:s3:::{bucket_name}",
                        },
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": "*"},
                            "Action": [
                                "s3:GetObject",
                                "s3:PutObject",
                                "s3:DeleteObject",
                                "s3:ListMultipartUploadParts",
                                "s3:AbortMultipartUpload",
                            ],
                            "Resource": f"arn:aws:s3:::{bucket_name}/*",
                        },
                    ],
                }
                mc.make_bucket(bucket_name)
                mc.set_bucket_policy(bucket_name, json.dumps(policy))
                logger.info(f'[MINIO] Created bucket {bucket_name}')
            
            mc.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=data,
                length=lenght,
                part_size=10*1024*1024,
                content_type='audio/mpeg'
            )
            
            logger.info(f'[MINIO] Uploaded file {object_name}')
        
        except Exception as e:
            logger.info(f'[MINIO] Error uploading file {object_name}')
            logger.info(e)
