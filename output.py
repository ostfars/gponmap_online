# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class KmlData(models.Model):
    geom = models.PointField(dim=3, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=-1, blank=True, null=True)
    p_owner = models.CharField(max_length=80, blank=True, null=True)
    p_type = models.CharField(max_length=80, blank=True, null=True)
    p_mount = models.CharField(max_length=80, blank=True, null=True)
    inform = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    geometry = models.GeometryField(srid=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kml_data'
