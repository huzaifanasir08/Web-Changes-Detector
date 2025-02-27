from django.contrib import admin
from .models import Web

@admin.register(Web)
class WebAdmin(admin.ModelAdmin):
    list_display = ('web_name', 'web_url')
    search_fields = ('web_name',)
