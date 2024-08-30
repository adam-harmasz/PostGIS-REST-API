from django.contrib.gis.db import models


class Point(models.Model):
    location = models.PointField(srid=4326)

    def __str__(self):
        return f"Point: {self.location}"
