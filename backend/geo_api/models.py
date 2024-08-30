from django.contrib.gis.db import models

DEFAULT_SRID = 4326


class Point(models.Model):
    location = models.PointField()

    def __str__(self):
        return f"Point: {self.location}"
