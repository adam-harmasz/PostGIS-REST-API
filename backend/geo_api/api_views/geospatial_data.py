from rest_framework import generics

from geo_api.models import Point
from geo_api.serializers.geospatial_data import PointSerializer


class PointListCreateAPIView(generics.ListCreateAPIView):
    queryset = Point.objects.all()
    serializer_class = PointSerializer


class PointRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
