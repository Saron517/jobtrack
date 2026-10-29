from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["company", "job_title", "status", "applied_on", "owner"]
    list_filter = ["status"]
    search_fields = ["company", "job_title"]