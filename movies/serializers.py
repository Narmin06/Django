from datetime import date

from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategorySerializer
from directors.models import Director
from directors.serializers import DirectorSerializer
from writers.models import Writer
from writers.serializers import WriterSerializer

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    # Nested, read-only representations of the related objects.
    category_detail = CategorySerializer(source='category', read_only=True)
    director_detail = DirectorSerializer(source='director', read_only=True)
    writers_detail = WriterSerializer(source='writers', many=True, read_only=True)

    # Final image to display: uploaded file (absolute URL) or external link.
    poster = serializers.SerializerMethodField()

    # Writable relations by primary key.
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    director = serializers.PrimaryKeyRelatedField(queryset=Director.objects.all())
    writers = serializers.PrimaryKeyRelatedField(
        queryset=Writer.objects.all(), many=True, required=False
    )

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'content', 'release_year',
            'image_url', 'poster', 'youtube_link',
            'category', 'director', 'writers',
            'category_detail', 'director_detail', 'writers_detail',
            'average_rating', 'rating_count',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'poster', 'average_rating', 'rating_count',
            'created_at', 'updated_at',
        ]

    def get_poster(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return obj.image_url or None

    def validate_image_url(self, value):
        if value and not value.lower().startswith(('http://', 'https://')):
            raise serializers.ValidationError('Image URL must start with http(s).')
        return value

    def validate_title(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError(
                'Title must be at least 2 characters long.'
            )
        return value

    def validate_content(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError(
                'Content must be at least 10 characters long.'
            )
        return value

    def validate_release_year(self, value):
        if value is None:
            return value
        if value < 1888 or value > date.today().year + 5:
            raise serializers.ValidationError('Release year is not valid.')
        return value

    def validate_youtube_link(self, value):
        if value and not any(d in value for d in ('youtube.com', 'youtu.be')):
            raise serializers.ValidationError(
                'Link must be a valid YouTube URL.'
            )
        return value
