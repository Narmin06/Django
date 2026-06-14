import django_filters

from .models import Movie


class MovieFilter(django_filters.FilterSet):
    """Filter movies by category, director, writer and release year."""

    category = django_filters.NumberFilter(field_name='category__id')
    director = django_filters.NumberFilter(field_name='director__id')
    writer = django_filters.NumberFilter(field_name='writers__id')
    year = django_filters.NumberFilter(field_name='release_year')
    min_rating = django_filters.NumberFilter(
        field_name='average_rating', lookup_expr='gte'
    )

    class Meta:
        model = Movie
        fields = ['category', 'director', 'writer', 'year', 'min_rating']
