from django.db import models

from categories.models import Category
from directors.models import Director
from writers.models import Writer


class Movie(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(help_text='Plot / description of the movie')
    release_year = models.PositiveIntegerField(null=True, blank=True)

    image = models.ImageField(
        upload_to='movies/', null=True, blank=True,
        help_text='Upload an image file (multipart/form-data)',
    )
    image_url = models.URLField(
        blank=True, help_text='External image URL (alternative to upload)',
    )
    youtube_link = models.URLField(blank=True, help_text='Trailer / YouTube URL')

    @property
    def poster(self):
        """Return the uploaded image if present, otherwise the external URL."""
        if self.image:
            return self.image.url
        return self.image_url or None

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='movies'
    )
    director = models.ForeignKey(
        Director, on_delete=models.PROTECT, related_name='movies'
    )
    writers = models.ManyToManyField(Writer, related_name='movies', blank=True)

    # Denormalised aggregate kept in sync by the Rating model.
    average_rating = models.FloatField(default=0)
    rating_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def update_rating_stats(self):
        """Recompute average_rating / rating_count from related ratings."""
        from django.db.models import Avg

        agg = self.ratings.aggregate(avg=Avg('score'), count=models.Count('id'))
        self.average_rating = round(agg['avg'] or 0, 2)
        self.rating_count = agg['count'] or 0
        self.save(update_fields=['average_rating', 'rating_count'])
