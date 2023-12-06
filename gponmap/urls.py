from django.urls import path
from gponmap.views import GponmapView, QgisMapView, QgisNewMap, MapEditor, KMLEditor, KMLToDB, KMLftGeoman, EditKML

app_name = "gponmap"

urlpatterns = [
    path("map/", GponmapView.as_view()),
    path('qgis_test/', QgisMapView.as_view()),
    path('qgis_new/', QgisNewMap.as_view()),
    path('map_editor/', MapEditor.as_view()),
    path('kml_editor/', KMLEditor.as_view()),
    path('kml_to_db/', KMLToDB.as_view()),
    path('kml_ft_geoman/', KMLftGeoman.as_view()),
    path('edit_kml/', EditKML.as_view()),

]
