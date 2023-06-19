from django.contrib.gis import admin
from gponmap.models import Point

@admin.register(Point)
class MarkerAdmin(admin.GISModelAdmin):
    list_display = ("name", "location")
