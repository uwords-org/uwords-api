from django.contrib import admin
from category_api.models import Category, CatWord


class InlineCatWord(admin.StackedInline):
    model = CatWord
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [InlineCatWord]
    list_display = ("id", "title",)
    search_fields = ("title", )
    ordering = ("id", )


class CatWordAdmin(admin.ModelAdmin):
    list_display = ("id", "ruValue", "category")
    search_fields = ("ruValue", "category", )
    list_filter = ("category", )
    ordering = ("id", )


admin.site.register(Category, CategoryAdmin)
admin.site.register(CatWord, CatWordAdmin)
