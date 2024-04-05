from django.contrib import admin
from words_api.models import Word, UserWord


class WordAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "audio", )
    search_fields = ("value", )
    ordering = ("id", )


class UserWordAdmin(admin.ModelAdmin):
    list_display = ("id", "word", "user", "isChecked", )
    search_fields = ("word__value",)
    ordering = ("id",)


admin.site.register(Word, WordAdmin)
admin.site.register(UserWord, UserWordAdmin)
