from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.generics import ListAPIView
from django.http import JsonResponse

from django.http import HttpResponse
from django.contrib.gis.geos import MultiLineString
from django.contrib.gis.db.models.functions import AsKML
import subprocess

from .models import QgisPoint, QgisPointsLineInfo, QgisLine, QgisPolygon, ColorLine, RealLine, QgisCoupling, QgisBStation, QgisOSB, QgisOSKM, KMLLine
from .serializers import QgisPointSerializer, QgisPointsLineInfoSerializer, QgisLineSerializer, QgisPolygonSerializer, ColorLineSerializer, RealLineSerializer, QgisCouplingSerializer, QgisBStationSerializer, QgisOSBSerializer, QgisOSKMSerializer


class GponmapView(TemplateView):
    template_name = "map.html"


class QgisMapView(TemplateView):
    template_name = "qgis_test.html"


class QgisNewMap(TemplateView):
    template_name = "qgis_new.html"


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


def kml_lines(request):
    # Извлекаем мультилинии из базы данных
    multilines = KMLLine.objects.all()

    # Преобразуем мультилинии в KML
    kml = '<kml xmlns="http://www.opengis.net/kml/2.2">'
    kml += '<Document>'
    for multiline in multilines:
        kml += '<Placemark>'
        kml += '<name>Линия</name>'
        kml += '<description>ВОК' + multiline.capacity + '</description>'
        kml += AsKML(multiline.geom)
        kml += '</Placemark>'
    kml += '</Document>'
    kml += '</kml>'

    # Возвращаем KML-документ в HTTP-ответе
    response = HttpResponse(content_type='application/vnd.google-earth.kml+xml')
    response['Content-Disposition'] = 'attachment; filename="export.kml"'
    response.write(kml)
    return response


def pm4(request):
    return render(request, 'PM4.html')


def oskm10(request):
    return render(request, 'oskm_10.html')


def export_to_kml(request):
    # table_name = request.GET.get('table_name', '')
    table_name = 'couplings_all'
    kml_path = '/home/vladimir/output.kml'

    command = f'ogr2ogr -f KML {kml_path} PG:"dbname=<gpondb> user=<postgres> password=<e2ad7c2437>" -sql "SELECT * FROM {table_name}"'
    subprocess.call(command, shell=True)

    # Отправка KML-файла как ответа API
    with open(kml_path, 'rb') as file:
        response = HttpResponse(file, content_type='application/vnd.google-earth.kml+xml')
        response['Content-Disposition'] = f'attachment; filename="{table_name}.kml"'
        return response
