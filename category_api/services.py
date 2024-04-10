from category_api.models import CatWord


class CatWordService:

    @staticmethod
    def get_category_by_word(ruValue: str) -> str:
        word = CatWord.objects.filter(ruValue=ruValue).first()

        if word:
            return word.category
        
        else:
            return None