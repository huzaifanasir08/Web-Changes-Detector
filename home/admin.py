# admin.py
from django.contrib import admin
from .models import Check
from home.task import run_auto_check

@admin.register(Check)
class ChecksAdmin(admin.ModelAdmin):
    list_display = ('web_name', 'status', 'result', 'last_check')
    list_filter = ('web_name',)
