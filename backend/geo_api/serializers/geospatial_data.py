from rest_framework_gis.serializers import GeoFeatureModelSerializer

from geo_api.models import Point


class PointSerializer(GeoFeatureModelSerializer):
    """ A class to serialize points as GeoJSON compatible data """

    class Meta:
        model = Point
        geo_field = "location"
        fields = ('id', 'location')
