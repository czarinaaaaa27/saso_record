from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, ActivityParticipationViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet)
router.register(r'participations', ActivityParticipationViewSet)

urlpatterns = router.urls
