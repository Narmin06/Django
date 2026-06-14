from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Writer
from .serializers import WriterSerializer


class WriterViewSet(viewsets.ModelViewSet):
    """CRUD for writers. Public read, authenticated write."""

    queryset = Writer.objects.all()
    serializer_class = WriterSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
