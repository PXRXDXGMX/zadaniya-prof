from django.contrib import admin

from .models import GroomRequest


@admin.register(GroomRequest)
class GroomRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "pet_name", "owner", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("pet_name", "owner__username")
