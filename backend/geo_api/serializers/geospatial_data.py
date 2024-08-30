from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers

from geo_api.models import DBPoint, DBLineString, DBPolygon


class PointSerializer(GeoFeatureModelSerializer):
    """A class to serialize points as GeoJSON compatible data"""

    class Meta:
        model = DBPoint
        geo_field = "location"
        fields = ("id", "location")


class LineStringSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = DBLineString
        geo_field = "line"
        fields = ("id", "name", "line")


class PolygonSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = DBPolygon
        geo_field = "polygon"
        fields = ("id", "name", "polygon")


class LineStringIdsSerializer(serializers.Serializer):
    lines = serializers.ListField(child=serializers.IntegerField(min_value=1), allow_empty=False)


class PontIdsSerializer(serializers.Serializer):
    points = serializers.ListField(child=serializers.IntegerField(min_value=1), allow_empty=False)
