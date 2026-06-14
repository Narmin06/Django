from rest_framework.routers import DefaultRouter

from .views import DirectorViewSet

router = DefaultRouter()
router.register('directors', DirectorViewSet, basename='director')

urlpatterns = router.urls
