from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from .models import QgisPoint, QgisPointsLineInfo, QgisLine, QgisPolygon, ColorLine, RealLine, QgisCoupling, QgisBStation, QgisOSB, QgisOSKM
from .serializers import QgisPointSerializer, QgisPointsLineInfoSerializer, QgisLineSerializer, QgisPolygonSerializer, ColorLineSerializer, RealLineSerializer, QgisCouplingSerializer, QgisBStationSerializer, QgisOSBSerializer, QgisOSKMSerializer


class GponmapView(TemplateView):
    template_name = "map.html"


class QgisMapView(TemplateView):
    template_name = "qgis_test.html"


class QgisPointAPIView(ListAPIView):
    queryset = QgisPoint.objects.all()
    serializer_class = QgisPointSerializer


class QgisPointsLineInfoAPIView(ListAPIView):
    queryset = QgisPointsLineInfo.objects.all()
    serializer_class = QgisPointsLineInfoSerializer


class QgisLineAPIView(ListAPIView):
    queryset = QgisLine.objects.all()
    serializer_class = QgisLineSerializer
    
    
class QgisPolygonAPIView(ListAPIView):
    queryset = QgisPolygon.objects.all()
    serializer_class = QgisPolygonSerializer
    
    
class ColorLineAPIView(ListAPIView):
    queryset = ColorLine.objects.all()
    serializer_class = ColorLineSerializer


class RealLineAPIView(ListAPIView):
    queryset = RealLine.objects.all()
    serializer_class = ColorLineSerializer


class QgisCouplingAPIView(ListAPIView):
    queryset = QgisCoupling.objects.all()
    serializer_class = QgisCouplingSerializer


class QgisBStationAPIView(ListAPIView):
    queryset = QgisBStation.objects.all()
    serializer_class = QgisBStationSerializer
    

class QgisOSBAPIView(ListAPIView):
    queryset = QgisOSB.objects.all()
    serializer_class = QgisOSBSerializer


class QgisOSKMAPIView(ListAPIView):
    queryset = QgisOSKM.objects.all()
    serializer_class = QgisOSKMSerializer