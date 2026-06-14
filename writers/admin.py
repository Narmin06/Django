from django.contrib import admin

from .models import Writer


@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']
