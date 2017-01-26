from django.contrib import admin
from rango.models import Page, Category

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'views', 'likes')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
