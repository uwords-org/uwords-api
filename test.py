from googletrans import Translator


translator = Translator()


translated = translator.translate('Hello', src='english', dest='russian')

print(translated.text)
