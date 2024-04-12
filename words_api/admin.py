from django.contrib import admin
from words_api.models import Word, UserWord
from django.utils.safestring import mark_safe


class WordAdmin(admin.ModelAdmin):
    list_display = ("id", "enValue", "ruValue", "get_link", )

    def get_link(self, obj):
        return mark_safe(f'<a href={obj.audioLink}>{obj.audioLink.split("/")[-1]}</a>')
    
    get_link.short_description = "Ссылка на аудиозапись"

    search_fields = ("enValue", "ruValue", )
    ordering = ("id", )


class UserWordAdmin(admin.ModelAdmin):
    list_display = ("id", "word", "user", "frequency", "isChecked", )
    search_fields = ("word__enValue", "word__ruValue",)
    ordering = ("id",)


admin.site.register(Word, WordAdmin)
admin.site.register(UserWord, UserWordAdmin)
