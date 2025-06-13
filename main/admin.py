from django.contrib import admin
from .models import SlangModel
# Register your models here.
@admin.register(SlangModel)
class SlangModelAdmin(admin.ModelAdmin):
    list_display = ['slang', 'definition']