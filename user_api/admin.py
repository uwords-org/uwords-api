from django.contrib import admin
from user_api.models import User
from words_api.models import UserWord


class UserWordInline(admin.StackedInline):
    model = UserWord
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [UserWordInline]
    list_display = ("id", "name", "email", "is_active", "created_at", )
    search_fields = ("name", "email",)
    # ordering = ("id", )
    # exclude = ("password", )


admin.site.register(User, UserAdmin)
