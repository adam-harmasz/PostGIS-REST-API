from django.contrib import admin

from geo_api.models import DBPoint, DBLineString, DBPolygon


admin.site.register(DBPoint)
admin.site.register(DBLineString)
admin.site.register(DBPolygon)
