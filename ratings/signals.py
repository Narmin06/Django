from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Rating


@receiver(post_save, sender=Rating)
@receiver(post_delete, sender=Rating)
def refresh_movie_rating(sender, instance, **kwargs):
    """Keep the movie's average_rating / rating_count in sync."""
    instance.movie.update_rating_stats()
