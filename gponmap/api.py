from rest_framework import routers
from gponmap.viewsets import PointViewSet

router = routers.DefaultRouter()
router.register(r"gponmap", PointViewSet)

urlpatterns = router.urls
