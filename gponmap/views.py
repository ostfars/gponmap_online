from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from rest_framework.generics import ListAPIView
from django.http import JsonResponse

from django.http import HttpResponse
from django.contrib.gis.geos import MultiLineString, LineString, Point

from django.contrib.gis.geos import GEOSGeometry

from django.contrib.gis.shortcuts import render_to_kml
from django.contrib.gis.db.models.functions import AsKML
from django.contrib.gis.gdal import DataSource

from lxml import etree

import binascii

import subprocess

from .models import QgisPoint, QgisPointsLineInfo, QgisLine, QgisPolygon, ColorLine, RealLine, QgisCoupling, \
    QgisBStation, QgisOSB, QgisOSKM, KMLLine, AddKMLData, UploadKMLPoint, UploadKMLLine, UploadKMLPolygon
from .serializers import QgisPointSerializer, QgisPointsLineInfoSerializer, QgisLineSerializer, QgisPolygonSerializer, \
    ColorLineSerializer, RealLineSerializer, QgisCouplingSerializer, QgisBStationSerializer, QgisOSBSerializer, QgisOSKMSerializer

from .forms import KMLLayerForm, KMLUploadForm


class Test(TemplateView):
    template_name = "test_template.html"


class EditKML(TemplateView):
    template_name = "edit_kml.html"


class IndexView(TemplateView):
    template_name = "index.html"


class GponmapView(TemplateView):
    template_name = "map.html"


class QgisMapView(TemplateView):
    template_name = "qgis_test.html"


class QgisNewMap(TemplateView):
    template_name = "qgis_new.html"

class MapEditor(TemplateView):
    template_name = "map_editor.html"


class KMLEditor(TemplateView):
    template_name = "kml_editor.html"


class KMLToDB(TemplateView):
    template_name = "kml_to_db.html"


class KMLftGeoman(TemplateView):
    template_name = "kml_ft_geoman.html"


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
            kml += f'{feature.geom.kml}\n'
            kml += '</Placemark>\n'

    # Закрытие KML-документф.
    kml += '</Document>\n</kml>'

    # Возврат KML в ответе.
    response = HttpResponse(kml, content_type='application/vnd.google-earth.kml+xml')
    response['Content-Disposition'] = 'attachment; filename="data.kml"'
    return response


def export_kml(request):
    kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2">'
    kml += '<Document>'
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
            kml += '<Placemark>'
            kml += '<name><![CDATA[' + obj.name + ']]></name>'
            if obj.kross is not None:
                kml += '<description><![CDATA[<b>Кросс: </b>' + obj.kross + ']]></description>'
            kml += '{}</Placemark>'.format(obj.geom_kml)
        kml += '</Folder>'

    if 'layer6' in request.GET:
        kml += '<Folder>'
        layer6 = QgisPolygon.objects.annotate(geom_kml=AsKML('geom'))
        for obj in layer6:
            kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
        kml += '</Folder>'

    if 'layer7' in request.GET:
        kml += '<Folder>'
        layer7 = ColorLine.objects.annotate(geom_kml=AsKML('geom'))
        for obj in layer7:
            kml += '<Placemark>'
            if obj.capacity is not None:
                kml += '<name><![CDATA[<b>ВОК' + obj.capacity + '</b>]]></name>'

            kml += '<description><![CDATA[<b>Статус: </b>'
            if obj.status == 0:
                kml += 'проект'
            elif obj.status == 1:
                kml += 'построено'
            if obj.cable_mark is not None:
                kml += '<br><b>Кабель: </b>' + obj.cable_mark
            kml += ']]></description>'

            kml += '<Style><LineStyle><color>FF' + obj.color[1:] + '</color><width>4</width></LineStyle></Style>'
            kml += '{}</Placemark>'.format(obj.geom_kml)
        kml += '</Folder>'

    if 'layer8' in request.GET:
        kml += '<Folder>'
        layer8 = RealLine.objects.annotate(geom_kml=AsKML('geom'))
        for obj in layer8:
            kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
        kml += '</Folder>'
    kml += '</Document>'
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


# def upload_kml(request):
#     if request.method == 'POST':
#         form = KMLUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             kml_file = request.FILES['kml_file']
#             try:
#                 tree = etree.parse(kml_file)
#                 root = tree.getroot()
#                 # print(root)
#
#                 # folder = root.find(".//{http://www.opengis.net/kml/2.2}Folder")
#                 # print(folder)
#
#                 kml_points = root.findall(".//{http://www.opengis.net/kml/2.2}Point")
#                 print(kml_points)
#
#                 for kml_point in kml_points:
#                     # name = placemark.find("{http://www.opengis.net/kml/2.2}name").text
#                     coordinates = kml_point.find(".//{http://www.opengis.net/kml/2.2}coordinates").text
#                     coordinates = coordinates.strip()
#                     lon, lat, *_ = coordinates.split(',')  # KML координаты: долгота, широта, высота
#
#                     # Создаем объект Point
#                     point = Point(float(lon), float(lat), 0)
#                     print(point)
#
#                     # Этот код ддля postgis не нужен
#                     # wkb = point.wkb
#                     # wkb_hex_upper = binascii.hexlify(wkb).decode().upper()
#                     # print(wkb_hex_upper)
#
#                     try:
#                         UploadKMLPoint.objects.create(geom=point)
#                     except Exception as e:
#                         print(f"Ошибка при создании записи: {e}")
#
#
#                 # return redirect('success_page')  # Перенаправьте на страницу успешной загрузки
#             except Exception as e:
#                 return render(request, 'upload_kml.html', {'form': form, 'error_message': f"Ошибка при парсинге KML: {e}"})
#     else:
#         form = KMLUploadForm()
#     return render(request, 'upload_kml.html', {'form': form})


def upload_kml(request):
    if request.method == 'POST':
        form = KMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            kml_file = request.FILES['kml_file']
            try:
                tree = etree.parse(kml_file)
                root = tree.getroot()
                # print(root)

                # folder = root.find(".//{http://www.opengis.net/kml/2.2}Folder")
                # print(folder)

                # multi_line_strings = folder.findall(".//{http://www.opengis.net/kml/2.2}MultiGeometry")
                # for multi_line_string in multi_line_strings:
                line_strings = root.findall(".//{http://www.opengis.net/kml/2.2}LineString")
                # print(line_strings)
                for line_string in line_strings:
                    coordinates = line_string.find(".//{http://www.opengis.net/kml/2.2}coordinates").text
                    coordinates = coordinates.strip()
                    points = coordinates.split()  # Координаты для LineString разделены пробелами
                    line_points = []

                    for point in points:
                        lon, lat, *_ = point.split(',')
                        # print(point)
                        line_points.append((float(lon), float(lat)))  # Добавляем координаты в список

                    # print(line_points)

                    # Создаем объект MultiLineString
                    line_string = LineString(line_points)
                    print(line_string)

                    try:
                        UploadKMLLine.objects.create(geom=line_string)
                    except Exception as e:
                        print(f"Ошибка при создании записи мультилинии: {e}")

                # Теперь обрабатываем точки
                points = root.findall(".//{http://www.opengis.net/kml/2.2}Point")
                for point in points:
                    coordinates = point.find(".//{http://www.opengis.net/kml/2.2}coordinates").text
                    coordinates = coordinates.strip()
                    lon, lat, *_ = coordinates.split(',')  # KML координаты: долгота, широта, высота

                    # Создаем объект Point
                    point_obj = Point(float(lon), float(lat), 0)

                    try:
                        AddKMLPoint.objects.create(geom=point_obj)
                    except Exception as e:
                        print(f"Ошибка при создании записи точки: {e}")

            except Exception as e:
                return render(request, 'upload_kml.html', {'form': form, 'error_message': f"Ошибка при парсинге KML: {e}"})
    else:
        form = KMLUploadForm()
    return render(request, 'upload_kml.html', {'form': form})


def google_earth_kml(request):
    kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2">'

    #     kml += '<Folder>'
    #     layer1 = QgisPointsLineInfo.objects.annotate(geom_kml=AsKML('geom'))
    #     for obj in layer1:
    #         kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
    #     kml += '</Folder>'

    kml += '<Document>'
    kml += '<Folder>'
    kml += '<name>ОСБ</name>'
    osb_layer = QgisOSB.objects.annotate(geom_kml=AsKML('geom'))
    for obj in osb_layer:
        kml += '<Placemark>'
        if isinstance(obj.osb, str):
            kml += '<name>'
            kml += obj.osb
            kml += '</name>'
        kml += '<Style><IconStyle><color>ff00eadf</color></IconStyle></Style>'
        kml += '{}</Placemark>'.format(obj.geom_kml)

    kml += '</Folder>'

    kml += '<Folder>'
    kml += '<name>ОСКМ</name>'
    oskm_layer = QgisOSKM.objects.annotate(geom_kml=AsKML('geom'))
    for obj in oskm_layer:
        kml += '<Placemark>'
        if isinstance(obj.oskm, str):
            kml += '<name>'
            kml += obj.oskm
            kml += '</name>'
        kml += '<Style><IconStyle><color>ff00ff00</color></IconStyle></Style>'
        kml += '{}</Placemark>'.format(obj.geom_kml)
    kml += '</Folder>'

    kml += '<Folder>'
    kml += '<name>Муфты</name>'
    coupler_layer = QgisCoupling.objects.annotate(geom_kml=AsKML('geom'))
    for obj in coupler_layer:
        kml += '<Placemark>'
        if isinstance(obj.coupling, str):
            kml += '<name>'
            kml += obj.coupling
            kml += '</name>'
        kml += '<Style><IconStyle><color>ff0000ff</color></IconStyle></Style>'
        kml += '{}</Placemark>'.format(obj.geom_kml)

    kml += '</Folder>'

    kml += '<Folder>'
    kml += '<name>Базовые станции</name>'
    bs_layer = QgisBStation.objects.annotate(geom_kml=AsKML('geom'))
    for obj in bs_layer:
        kml += '<Placemark>'
        kml += '<name>'
        kml += obj.name
        kml += '</name>'
        kml += '{}</Placemark>'.format(obj.geom_kml)
    kml += '</Folder>'

    kml += '<Folder>'
    kml += '<name>Покрытие</name>'
    polygon_layer = QgisPolygon.objects.annotate(geom_kml=AsKML('geom'))
    for obj in polygon_layer:
        kml += '<Placemark>'
        kml += '<description><![CDATA['
        if obj.p_oskm is not None:
            kml += obj.p_oskm
        kml += ']]></description>'
        kml += '<Style><PolyStyle><color>B3' + obj.color[1:] + '</color><outline>1</outline></PolyStyle></Style>'
        kml += '{}</Placemark>'.format(obj.geom_kml)
    kml += '</Folder>'

    kml += '<Folder>'
    kml += '<name>Линии</name>'
    line_layer = ColorLine.objects.annotate(geom_kml=AsKML('geom'))
    for obj in line_layer:
        kml += '<Placemark>'
        if obj.capacity is not None:
            kml += '<name><![CDATA[<b>ВОК' + obj.capacity + '</b>]]></name>'

        kml += '<description><![CDATA[<b>Статус: </b>'
        if obj.status == 0:
            kml += 'проект'
        elif obj.status == 1:
            kml += 'построено'
        if obj.cable_mark is not None:
            kml += '<br><b>Кабель: </b>' + obj.cable_mark
        kml += ']]></description>'

        kml += '<Style><LineStyle><color>FF' + obj.color[1:] + '</color><width>4</width></LineStyle></Style>'
        kml += '{}</Placemark>'.format(obj.geom_kml)
    kml += '</Folder>'
    #
    # if 'layer8' in request.GET:
    #     kml += '<Folder>'
    #     layer8 = RealLine.objects.annotate(geom_kml=AsKML('geom'))
    #     for obj in layer8:
    #         kml += '<Placemark>{}</Placemark>'.format(obj.geom_kml)
    #     kml += '</Folder>'

    kml += '</Document>'
    kml += '</kml>'
    response = HttpResponse(kml, content_type='application/vnd.google-earth.kml+xml')
    return response