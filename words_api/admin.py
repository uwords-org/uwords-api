from django.contrib import admin
from words_api.models import Word, UserWord


class WordAdmin(admin.ModelAdmin):
    list_display = ("id", "enValue", "ruValue", "audioLink", )
    search_fields = ("enValue", "ruValue", )
    ordering = ("id", )


class UserWordAdmin(admin.ModelAdmin):
    list_display = ("id", "word", "user", "frequency", "isChecked", )
    search_fields = ("word__enValue", "word__ruValue",)
    ordering = ("id",)


admin.site.register(Word, WordAdmin)
admin.site.register(UserWord, UserWordAdmin)
