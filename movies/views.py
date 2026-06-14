from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .filters import MovieFilter
from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """
    CRUD for movies plus search, filtering, pagination and a top-10 endpoint.

    Public read, authenticated write.

    Query params:
      ?search=<title>            search by title
      ?category=<id>             filter by category
      ?director=<id>             filter by director
      ?writer=<id>               filter by writer
      ?year=<year>               filter by release year
      ?min_rating=<float>        movies with average_rating >= value
      ?ordering=-average_rating  order results
    """

    queryset = (
        Movie.objects.select_related('category', 'director')
        .prefetch_related('writers')
        .all()
    )
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'release_year', 'average_rating', 'created_at']

    @action(detail=False, methods=['get'])
    def top(self, request):
        """GET /api/movies/top/ -> top 10 movies by average rating."""
        top_movies = self.get_queryset().order_by('-average_rating', '-rating_count')[:10]
        serializer = self.get_serializer(top_movies, many=True)
        return Response(serializer.data)
