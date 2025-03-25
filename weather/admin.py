from django.contrib import admin
from .models import Weather

@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ("city", "temperature", "description", "last_updated")
    search_fields = ("city", "country")
    list_filter = ("country", "is_day")
    ordering = ("-last_updated",)
