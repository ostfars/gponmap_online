from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.generics import ListAPIView
from django.http import JsonResponse

from django.http import HttpResponse
from django.contrib.gis.geos import MultiLineString

from django.contrib.gis.geos import GEOSGeometry

from django.contrib.gis.shortcuts import render_to_kml
from django.contrib.gis.db.models.functions import AsKML
from django.contrib.gis.gdal import DataSource

import subprocess

from .models import QgisPoint, QgisPointsLineInfo, QgisLine, QgisPolygon, ColorLine, RealLine, QgisCoupling, QgisBStation, QgisOSB, QgisOSKM, KMLLine
from .serializers import QgisPointSerializer, QgisPointsLineInfoSerializer, QgisLineSerializer, QgisPolygonSerializer, ColorLineSerializer, RealLineSerializer, QgisCouplingSerializer, QgisBStationSerializer, QgisOSBSerializer, QgisOSKMSerializer

from .forms import KMLLayerForm


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
    serializer_class = RealLineSerializer


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
    multilines = ColorLine.objects.all()

    # Преобразуем мультилинии в KML
    kml = '<kml xmlns="http://www.opengis.net/kml/2.2">'
    kml += '<Document>'
    for multiline in multilines:
        kml += '<Placemark>'
        kml += '<name>Линия</name>'
        kml += '<description>ВОК' + multiline.capacity + '</description>'
        kml += multiline.geom_kml
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
    table_name = request.GET.get('table_name', '')
    # table_name = 'couplings_all'
    kml_path = '/home/vladimir/output.kml'

    command = f'ogr2ogr -f KML {kml_path} PG:"dbname=<gpondb> user=<postgres> password=<e2ad7c2437>" -sql "SELECT * FROM {table_name}"'
    subprocess.call(command, shell=True)

    # Отправка KML-файла как ответа API
    with open(kml_path, 'rb') as file:
        response = HttpResponse(file, content_type='application/vnd.google-earth.kml+xml')
        response['Content-Disposition'] = f'attachment; filename="{table_name}.kml"'
        return response


def render_line_to_kml(request):
    color_lines = ColorLine.objects.all()
    kml = render_to_kml('gponmap/lines.kml', {'locations': color_lines})
    response = HttpResponse(kml, content_type='application/vnd.google-earth.kml+xml')
    response['Content-Disposition'] = 'attachment; filename="lines.kml"'
    return response


def kml_all(request):

    polygons = QgisPolygon.objects.all()
    multilines = ColorLine.objects.all()
    points = QgisPointsLineInfo.objects.all()

    geometries = []

    # Добавление полигонов
    for polygon in polygons:
        geometries.append(polygon.geom)

    # Добавление мультилиний
    for multilinestring in multilines:
        geometries.append(multilinestring.geom)

    # Добавление точек
    for point in points:
        geometries.append(point.geom)

    # Создание геометрической коллекции
    collection = GeometryCollection(geometries)

    kml = collection.kml
    response = HttpResponse(kml, content_type='application/vnd.google-earth.kml+xml')
    response['Content-Disposition'] = 'attachment; filename="geometries.kml"'
    return response


def download_kml_view(request):
    # Получение данные из каждой таблицы PostGIS.
    # pillars = QgisPointsLineInfo.objects.all()
    # couplers = QgisCoupling.objects.all()
    # oskm = QgisOSKM.objects.all()
    # osb = QgisOSB.objects.all()
    # bstations = QgisBStation.objects.all()
    # polygons = QgisPolygon.objects.all()
    # multilines = ColorLine.objects.all()

    # Создание пустого KML-документа.
    kml = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'

    # Загрузка данных из таблиц PostGIS с разными геометрическими типами.
    data_sources = [
        DataSource('infopoints_all'),
        DataSource('colorlines_all'),
        DataSource('polygons_info_all'),
    ]

    # Добавление данных каждой таблицы в KML.
    # kml += LayerMapping(pillars, {'geom': 'Point'}, name='Опоры').kml()
    # kml += LayerMapping(couplers, {'geom': 'Point'}, name='Муфты').kml()
    # kml += LayerMapping(oskm, {'geom': 'Point'}, name='ОСКМ').kml()
    # kml += LayerMapping(osb, {'geom': 'Point'}, name='ОСБ').kml()
    # kml += LayerMapping(bstations, {'geom': 'Point'}, name='Базовые станции').kml()
    # kml += LayerMapping(polygons, {'geom': 'Polygon'}, name='Покрытие').kml()
    # kml += LayerMapping(multilines, {'geom': 'MultiLineString'}, name='Линии').kml()

    for data_source in data_sources:
        layer = data_source[0]

        for feature in layer:
            kml += f'<Placemark>\n<name>{feature.name}</name>\n'
            kml += f'<description>{feature.description}</description>\n'
            kml += f'{feature.geom.kml}\n'  # Поле 'geom' должно содержать геометрию.
            kml += '</Placemark>\n'

    # Закрытие KML-документф.
    kml += '</Document>\n</kml>'

    # Возврат KML в ответе.
    response = HttpResponse(kml, content_type='application/vnd.google-earth.kml+xml')
    response['Content-Disposition'] = 'attachment; filename="data.kml"'
    return response


def export_kml(request):
    kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2">'

    if 'layer1' in request.GET:
        kml += '<Folder>'
        layer1 = QgisPointsLineInfo.objects.annotate(geom_kml=AsKML('geom'))
        for obj in layer1:
            kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
        kml += '</Folder>'

    if 'layer2' in request.GET:
        kml += '<Folder>'
        layer2 = QgisOSB.objects.annotate(geom_kml=AsKML('geom'))
        for obj in layer2:
            kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
        kml += '</Folder>'

    if 'layer3' in request.GET:
        kml += '<Folder>'
        layer3 = QgisOSKM.objects.annotate(geom_kml=AsKML('geom'))
        for obj in layer3:
            kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
        kml += '</Folder>'

    if 'layer4' in request.GET:
        kml += '<Folder>'
        layer4 = QgisCoupling.objects.annotate(geom_kml=AsKML('geom'))
        for obj in layer4:
            kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
        kml += '</Folder>'

    if 'layer5' in request.GET:
        kml += '<Folder>'
        layer5 = QgisBStation.objects.annotate(geom_kml=AsKML('geom'))
        for obj in layer5:
            kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
        kml += '</Folder>'

    if 'layer6' in request.GET:
        kml += '<Folder>'
        layer6 = QgisPolygon.objects.annotate(geom_kml=AsKML('geom'))
        for obj in layer6:
            kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
        kml += '</Folder>'

    # if 'layer7' in request.GET:
    #     kml += '<Folder>'
    #     layer7 = ColorLine.objects.annotate(geom_kml=AsKML('geom'))
    #     for obj in layer7:
    #         kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
    #     kml += '</Folder>'

    if 'layer7' in request.GET:

        layer7 = ColorLine.objects.all()

        kml += '<Folder>'
        for obj in layer7:
            kml += '<Placemark>'
            kml += '<name><b>ВОК' + multiline.capacity + '</b></name>'
            kml += '<description>ВОК' + multiline.capacity + '</description>'
            kml += multiline.geom_kml
            kml += '</Placemark>'


            kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
        kml += '</Folder>'

    if 'layer8' in request.GET:
        kml += '<Folder>'
        layer8 = RealLine.objects.annotate(geom_kml=AsKML('geom'))
        for obj in layer8:
            kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
        kml += '</Folder>'

    kml += '</kml>'
    response = HttpResponse(kml, content_type='application/vnd.google-earth.kml+xml')
    response['Content-Disposition'] = 'attachment; filename="export.kml"'
    return response


def kml_layer_selection(request):
    if request.method == 'POST':
        form = KMLLayerForm(request.POST)
        if form.is_valid():
            # Обработка выбранных слоев
            selected_layers = []
            if form.cleaned_data['layer1']:
                selected_layers.append('layer1')
            if form.cleaned_data['layer2']:
                selected_layers.append('layer2')
            if form.cleaned_data['layer3']:
                selected_layers.append('layer3')
            if form.cleaned_data['layer4']:
                selected_layers.append('layer4')
            if form.cleaned_data['layer5']:
                selected_layers.append('layer5')
            if form.cleaned_data['layer6']:
                selected_layers.append('layer6')
            if form.cleaned_data['layer7']:
                selected_layers.append('layer7')
            if form.cleaned_data['layer8']:
                selected_layers.append('layer8')

            # Выполнение экспорта KML с выбранными слоями

    else:
        form = KMLLayerForm()

    return render(request, 'layer_selection.html', {'form': form})