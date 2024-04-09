import uuid
import string
import logging
import pymorphy3
import subprocess

from gtts import gTTS
from pytube import YouTube
from librosa import get_duration
from googletrans import Translator
from speech_recognition import Recognizer, AudioFile

from user_api.services import UserService
from words_api.models import UserWord, Word
from uwords_api.instance import STOPWORDS


sr = Recognizer()



class AudioFileService:

    @staticmethod
    def upload_audio(audio: any, path: str) -> str:
        try:
            destination = open(path, "wb")
            
            for chunk in audio.chunks():
                destination.write(chunk)

            return path
        
        except Exception as e:
            logging.info(e)
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
            logging.info(e)
            return None
    
    @staticmethod
    def cut_audio(path: str, title: str) -> list[str]:
        files = []
        
        try:
            index = 0
            duration = get_duration(filename=path)
            
            while index * 30 < duration:
                out_path = f'output/{title}_{index}.wav'

                if (index + 1) * 30 < duration:
                    cmd = f'ffmpeg -ss {index * 30} -i {path} -t 30 -ac 1 {out_path} -y'
                else:
                    cmd = f'ffmpeg -ss {index * 30} -i {path} -ac 1 {out_path} -y'

                subprocess.call(cmd, shell=True)
                
                files.append(out_path)
                index += 1

            return files
        
        except Exception as e:
            logging.info(e)
            return None

    @staticmethod
    def convert_audio(path: str, title: str) -> str:
        try:
            out_path = f'output/{title}.wav'
            cmd = f'ffmpeg -i {path} -ac 1 {out_path} -y'
            
            subprocess.call(cmd, shell=True)
            
            return out_path
        
        except Exception as e:
            logging.info(e)
            return None
        
    @staticmethod
    def speech_to_text_en(filepath: str) -> str:
        try:
            with AudioFile(filepath) as source:
                audio_data = sr.record(source)
                text = sr.recognize_google(audio_data, language='en-US')
                
                return text.lower()
        
        except Exception as e:
            logging.info(e)
            return ' '
        
    @staticmethod
    def speech_to_text_ru(filepath: str) -> str:
        try:
            with AudioFile(filepath) as source:
                sr.adjust_for_ambient_noise(source, duration=0.2)
                audio_data = sr.record(source)
                text = sr.recognize_google(audio_data, language='ru-RU')
                
                return text.lower()
        
        except Exception as e:
            logging.info(e)
            return ' '
        
    @staticmethod
    def word_to_speech(word: str):
        try:
            tts = gTTS(text=word, lang='en', slow=False)
            path = f'audiofiles/{word.lower()}.mp3'
            tts.save(path)
            return path
        
        except:
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
            logging.info(e)
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
                logging.info(e)
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
        user_words = UserWord.objects.filter(user__id=user_id).all()
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
