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
from gponmap.views import QgisPointAPIView, QgisLineAPIView, QgisPolygonAPIView, ColorLineAPIView, QgisCouplingAPIView, QgisBStationAPIView, QgisOSBAPIView, QgisOSKMAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("gponmap.api")),
    path('gponmap/', include('gponmap.urls')),
    path('qgis_point', QgisPointAPIView.as_view(), name='points-api'),
    path('qgis_line', QgisLineAPIView.as_view(), name='lines-api'),
    path('qgis_polygon', QgisPolygonAPIView.as_view(), name='polygons-api'),
    path('qgis_colorline', ColorLineAPIView.as_view(), name='colorlines-api'),
    path('qgis_coupling', QgisCouplingAPIView.as_view(), name='couplings-api'),
    path('qgis_bstation', QgisBStationAPIView.as_view(), name='bstations-api'),
    path('qgis_osb', QgisOSBAPIView.as_view(), name='osb-api'),
    path('qgis_oskm', QgisOSKMAPIView.as_view(), name='oskm-api'),
]
