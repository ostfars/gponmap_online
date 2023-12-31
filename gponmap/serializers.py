from rest_framework_gis import serializers
from gponmap.models import Point, QgisPoint, QgisPointsLineInfo, QgisLine, QgisPolygon, ColorLine, RealLine, QgisCoupling, QgisBStation, QgisOSB, QgisOSKM, KMLLine


class PointSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        fields = ("id", "name")
        geo_field = "location"
        model = Point


class QgisPointSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = QgisPoint
        geo_field = 'geom'
        fields = '__all__'


class QgisPointsLineInfoSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = QgisPointsLineInfo
        geo_field = 'geom'
        fields = '__all__'


class QgisLineSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = QgisLine
        geo_field = 'geom'
        fields = '__all__'
        
        
class QgisPolygonSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = QgisPolygon
        geo_field = 'geom'
        fields = '__all__'
        
        
class ColorLineSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = ColorLine
        geo_field = 'geom'
        fields = '__all__'

        # def get_properties(self, instance, fields):
        #     properties = super().get_properties(instance, fields)
        #     properties['capacity'] = instance.capacity
        #     return properties
            

class RealLineSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = RealLine
        geo_field = 'geom'
        fields = '__all__'

        # def get_properties(self, instance, fields):
        #     properties = super().get_properties(instance, fields)
        #     properties['capacity'] = instance.capacity
        #     properties['']
        #     return properties


class QgisCouplingSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = QgisCoupling
        geo_field = 'geom'
        fields = '__all__'

        def get_properties(self, instance, fields):
            properties = super().get_properties(instance, fields)
            properties['coupling'] = instance.coupling
            return properties


class QgisBStationSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = QgisBStation
        geo_field = 'geom'
        fields = '__all__'

        
class QgisOSBSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = QgisOSB
        geo_field = 'geom'
        fields = '__all__'


class QgisOSKMSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = QgisOSKM
        geo_field = 'geom'
        fields = '__all__'


class KMLLineSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = KMLLine
        geo_field = 'geom'
        fields = '__all__'