from django.contrib import admin
from words_api.models import Word, UserWord


class WordAdmin(admin.ModelAdmin):
    list_display = ("id", "en_value", "ru_value", "audio", )
    search_fields = ("en_value", "ru_value", )
    ordering = ("id", )


class UserWordAdmin(admin.ModelAdmin):
    list_display = ("id", "word", "user", "frequency", "isChecked", )
    search_fields = ("word__en_value", "word__ru_value",)
    ordering = ("id",)


admin.site.register(Word, WordAdmin)
admin.site.register(UserWord, UserWordAdmin)
