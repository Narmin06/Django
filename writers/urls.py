from rest_framework.routers import DefaultRouter

from .views import WriterViewSet

router = DefaultRouter()
router.register('writers', WriterViewSet, basename='writer')

urlpatterns = router.urls
