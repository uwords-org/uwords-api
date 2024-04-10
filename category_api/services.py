from category_api.models import CatWord


class CatWordService:

    @staticmethod
    def get_category_by_word(ruValue: str) -> CatWord:
        catword = CatWord.objects.filter(ruValue=ruValue).first()

        if catword:
            return catword.category
        
        else:
            return None