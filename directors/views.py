from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Director
from .serializers import DirectorSerializer


class DirectorViewSet(viewsets.ModelViewSet):
    """CRUD for directors. Public read, authenticated write."""

    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
