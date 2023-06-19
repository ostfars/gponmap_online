from rest_framework import viewsets
from rest_framework_gis import filters

from gponmap.models import Point
from gponmap.serializers import PointSerializer


class PointViewSet(viewsets.ReadOnlyModelViewSet):
    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)
    queryset = Point.objects.all()
    serializer_class = PointSerializer
