from rest_framework import serializers
from category_api.serializers import CategorySerializer
from words_api.models import Word, UserWord


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = "__all__"


class UserWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWord
        fields = "__all__"

    word = WordSerializer()
    category = CategorySerializer()


class YoutubeAudioSerializer(serializers.Serializer):
    link = serializers.CharField(required=True)
    