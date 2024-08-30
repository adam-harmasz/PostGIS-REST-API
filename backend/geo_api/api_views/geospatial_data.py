from rest_framework import generics

from geo_api.models import DBPoint, DBLineString
from geo_api.serializers.geospatial_data import PointSerializer, LineStringSerializer


class PointListCreateAPIView(generics.ListCreateAPIView):
    queryset = DBPoint.objects.all()
    serializer_class = PointSerializer


class PointRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DBPoint.objects.all()
    serializer_class = PointSerializer


class LineStringListCreateAPIView(generics.ListCreateAPIView):
    queryset = DBLineString.objects.all()
    serializer_class = LineStringSerializer


class LineStringRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DBLineString.objects.all()
    serializer_class = LineStringSerializer
