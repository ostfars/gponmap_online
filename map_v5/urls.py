"""
URL configuration for map_v5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gponmap.views import QgisPointAPIView, QgisPointsLineInfoAPIView, QgisLineAPIView, QgisPolygonAPIView, \
    ColorLineAPIView, RealLineAPIView, QgisCouplingAPIView, QgisBStationAPIView, QgisOSBAPIView, QgisOSKMAPIView, \
    kml_lines, pm4, oskm10, export_to_kml, kml_all, download_kml_view, export_kml, kml_layer_selection, IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("api/", include("gponmap.api")),
    path('gponmap/', include('gponmap.urls')),
    path('qgis_point', QgisPointAPIView.as_view(), name='points-api'),
    path('qgis_line', QgisLineAPIView.as_view(), name='lines-api'),
    path('qgis_polygon', QgisPolygonAPIView.as_view(), name='polygons-api'),
    path('qgis_colorline', ColorLineAPIView.as_view(), name='colorlines-api'),
    path('qgis_realline', RealLineAPIView.as_view(), name='reallines-api'),
    path('qgis_coupling', QgisCouplingAPIView.as_view(), name='couplings-api'),
    path('qgis_bstation', QgisBStationAPIView.as_view(), name='bstations-api'),
    path('qgis_osb', QgisOSBAPIView.as_view(), name='osb-api'),
    path('qgis_oskm', QgisOSKMAPIView.as_view(), name='oskm-api'),
    path('qgis_point_info', QgisPointsLineInfoAPIView.as_view(), name='points-info-api'),
    path('kml_lines', kml_lines, name='export_lines_to_kml'),
    path('pm4/', pm4, name='PM4'),
    path('oskm10/', oskm10, name='oskm10'),
    path('api/export/', export_to_kml, name='export_to_kml'),
    path('kml_all', kml_all, name='kml_all'),

    path('download_kml/', download_kml_view, name='download_kml'),
    path('export_kml/', export_kml, name='export_kml'),
    path('kml_layer_selection/', kml_layer_selection, name='kml_layer_selection'),
    path('', IndexView.as_view(), name='index'),

    path('layer_selection.html', kml_layer_selection, name='kml_layer_selection'),
    path('export_kml.html', export_kml, name='export_kml'),

]
