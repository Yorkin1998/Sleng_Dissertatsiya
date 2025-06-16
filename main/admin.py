from django.contrib import admin
from .models import SlangModel, SlangSentence
# Register your models here.
@admin.register(SlangModel)
class SlangModelAdmin(admin.ModelAdmin):
    list_display = ['slang', 'definition']

@admin.register(SlangSentence)
class SlangSentenceAdmin(admin.ModelAdmin):
    list_display = ['slang', 'slang_word']