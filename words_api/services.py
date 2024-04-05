import uuid
import nltk
import string
import logging
import subprocess
from pytube import YouTube
from librosa import get_duration
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from speech_recognition import Recognizer, AudioFile

from words_api.models import UserWord


sr = Recognizer()
ps = SnowballStemmer("russian")


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')


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

            return download_path, filename
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
    def speech_to_text(filepath: str) -> str:

        with AudioFile(filepath) as source:

            audio_data = sr.record(source)
            text = sr.recognize_google(audio_data, language="ru")
            
            return text.lower()
        

class TextService:

    @staticmethod
    def remove_punctuation(text: str) -> str:
        spec_chars = string.punctuation + '\n\xa0«»\t—…' 
        return "".join([char for char in text if char not in spec_chars])
    
    @staticmethod
    def remove_stop_words(text: str) -> list[str]:
        ru_stopwords = stopwords.words("russian")
        return " ".join([word for word in text.split() if word not in ru_stopwords])
    
    @staticmethod
    def create_freq_dict(text: str) -> dict:
        freq_dict = {}
        
        for word in text.split():
            if word not in freq_dict.keys():
                freq_dict[word] = 1
            else:
                freq_dict[word] += 1

        return dict(sorted(freq_dict.items(), key=lambda x: x[1], reverse=True))
    
    @staticmethod
    def get_frequency_dict(text: str) -> dict:
        text_without_spec_chars = TextService.remove_punctuation(text=text)
        text_without_stop_words = TextService.remove_stop_words(text=text_without_spec_chars)

        freq_dict = TextService.create_freq_dict(text=text_without_stop_words)
        
        return freq_dict
        

class UserWordService:

    @staticmethod
    def get_user_words(user_id: int) -> list[UserWord]:
        user_words = UserWord.objects.filter(user__id=user_id).all()
        return user_words
    
    

        
    @staticmethod
    def sentence_splitter(text: str) -> list[str]:
        words = word_tokenize(text)

        result = []

        for w in words:
            result.append(f'{w} : {ps.stem(w)}')

        return result
