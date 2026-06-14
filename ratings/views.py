from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Rating
from .serializers import RatingSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only the rating's author may modify or delete it."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class RatingViewSet(viewsets.ModelViewSet):
    """
    CRUD for ratings.

    A user can rate each movie only once; the movie's average rating is
    updated automatically on create/update/delete (see ratings.signals).
    """

    queryset = Rating.objects.select_related('user', 'movie').all()
    serializer_class = RatingSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie', 'user', 'score']

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied('You can only edit your own rating.')
        serializer.save()
