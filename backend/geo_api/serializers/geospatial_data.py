from rest_framework_gis.serializers import GeoFeatureModelSerializer

from geo_api.models import DBPoint, DBLineString


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
