from django.contrib import admin

from geo_api.models import DBPoint, DBLineString


admin.site.register(DBPoint)
admin.site.register(DBLineString)
