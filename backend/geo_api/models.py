from django.contrib.gis.db import models

DEFAULT_SRID = 4326


class DBPoint(models.Model):
    location = models.PointField()

    def __str__(self):
        return f"Point: {self.location}"


class DBLineString(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    line = models.LineStringField()

    def __str__(self):
        return self.name
