from django.urls import path
from gponmap.views import GponmapView, QgisMapView, QgisNewMap, MapEditor

app_name = "gponmap"

urlpatterns = [
    path("map/", GponmapView.as_view()),
    path('qgis_test/', QgisMapView.as_view()),
    path('qgis_new/', QgisNewMap.as_view()),
    path('map_editor/', MapEditor.as_view()),
]
