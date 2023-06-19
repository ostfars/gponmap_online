from django.urls import path
from gponmap.views import GponmapView, QgisMapView

app_name = "gponmap"

urlpatterns = [
    path("map/", GponmapView.as_view()),
    path('qgis_test/', QgisMapView.as_view()),
]
