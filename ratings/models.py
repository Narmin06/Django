from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from movies.models import Movie


class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings'
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='ratings'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # A user can rate each movie only once.
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'], name='unique_user_movie_rating'
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.movie} ({self.score})'
