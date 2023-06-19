from django.contrib.gis.db import models


class Point(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField()

    def __str__(self):
        return self.name


class QgisPoints(models.Model):
    geom = models.PointField()

    def __str__(self):
        return self.geom

    class Meta:
        managed = False
        db_table = 'points_all'


class QgisPoint(models.Model):
    geom = models.PointField()

    class Meta:
        managed = False
        db_table = 'points_all'


class QgisLine(models.Model):
    geom = models.MultiLineStringField()

    class Meta:
        managed = False
        db_table = 'lines_all'
        

class QgisPolygon(models.Model):
    geom = models.MultiPolygonField()

    class Meta:
        managed = False
        db_table = 'polygons_all'
        
        
class ColorLine(models.Model):
    geom = models.MultiLineStringField()
    capacity = models.CharField(max_length=100)

    def __str__(self):
        return self.capacity

    class Meta:
        managed = False
        db_table = 'colorlines_all'
        
        
class QgisCoupling(models.Model):
    geom = models.PointField()
    coupling = models.CharField(max_length=100)

    def __str__(self):
        return self.coupling

    class Meta:
        managed = False
        db_table = 'couplings_all'


class QgisBStation(models.Model):
    geom = models.PointField()
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    kross = models.CharField(max_length=100)


    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'bstations_all'


class QgisOSB(models.Model):
    geom = models.PointField()
    osb = models.CharField(max_length=100)

    def __str__(self):
        return self.osb

    class Meta:
        managed = False
        db_table = 'osb_all'


class QgisOSKM(models.Model):
    geom = models.PointField()
    oskm = models.CharField(max_length=100)

    def __str__(self):
        return self.oskm

    class Meta:
        managed = False
        db_table = 'oskm_all'        
        
