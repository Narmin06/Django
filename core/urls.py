"""URL configuration for core project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth (JWT)
    path('api/auth/', include('users.urls')),

    # Core resources
    path('api/', include('categories.urls')),
    path('api/', include('directors.urls')),
    path('api/', include('writers.urls')),
    path('api/', include('movies.urls')),
    path('api/', include('ratings.urls')),

    # API schema / docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
