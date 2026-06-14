from django.contrib import admin
from django.utils.html import format_html

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'category', 'director',
        'average_rating', 'rating_count', 'release_year', 'preview',
    ]
    list_filter = ['category', 'director', 'release_year']
    search_fields = ['title', 'content']
    filter_horizontal = ['writers']
    readonly_fields = ['average_rating', 'rating_count', 'preview']
    # 'image' renders as a file-upload widget here in the admin.
    fields = [
        'title', 'content', 'release_year',
        'image', 'preview', 'image_url', 'youtube_link',
        'category', 'director', 'writers',
        'average_rating', 'rating_count',
    ]

    @admin.display(description='Poster')
    def preview(self, obj):
        if obj.poster:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:4px;" />',
                obj.poster,
            )
        return '—'
