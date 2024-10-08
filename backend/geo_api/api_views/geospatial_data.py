import json

from django.contrib.gis.db.models import Union
from django.contrib.gis.geos import GEOSGeometry
from django.db import transaction
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from geo_api.models import DBPoint, DBLineString, DBPolygon
from geo_api.serializers.geospatial_data import (
    PointSerializer,
    LineStringSerializer,
    PolygonSerializer,
    PontIdsSerializer,
    LineStringIdsSerializer,
)


class PointListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve a list of points or create a new point.
    This view provides GET and POST methods for listing all point objects
    or creating a new point object.
    """
    queryset = DBPoint.objects.all()
    serializer_class = PointSerializer


class PointRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific point.
    This view provides GET, PUT, PATCH, and DELETE methods for retrieving,
    updating, or deleting a specific point object.
    """
    queryset = DBPoint.objects.all()
    serializer_class = PointSerializer


class LineStringListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve a list of LineStrings or create a new one.
    This view provides GET and POST methods for listing all LineString objects
    or creating a new LineString object.
    """
    queryset = DBLineString.objects.all()
    serializer_class = LineStringSerializer


class LineStringRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific LineString.
    This view provides GET, PUT, PATCH, and DELETE methods for retrieving,
    updating, or deleting a specific LineString object.
    """
    queryset = DBLineString.objects.all()
    serializer_class = LineStringSerializer


class PolygonListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve a list of Polygon objects or create a new one.
    This view provides GET and POST methods for listing all Polygon objects
    or creating a new Polygon object.
    """
    queryset = DBPolygon.objects.all()
    serializer_class = PolygonSerializer


class PolygonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific Polygon.
    This view provides GET, PUT, PATCH, and DELETE methods for retrieving,
    updating, or deleting a specific Polygon object.
    """
    queryset = DBPolygon.objects.all()
    serializer_class = PolygonSerializer


class PolygonIntersectionApiView(APIView):
    """
    API View to handle the intersection of points with a specified polygon.

    This view allows users to check which points intersect with a given polygon
    by providing a list of point IDs in a POST request.
    """

    allowed_methods = ["post"]

    def post(self, request, pk, format="json"):
        """
        Handles POST request to find if any of given points are intersecting Polygon.

        Expects a JSON object with 'points' key containing list of Polygon IDs.

        Returns:
            - 200 OK: list of intersecting Points in GeoJSON format.
            - 400 Bad Request: If input is invalid.
            - 404 Not Found: If no Points are found or polygon is not found.
        """
        polygon = get_object_or_404(DBPolygon, pk=pk)
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": "No proper line ids have been provided!"}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            points = DBPoint.objects.filter(id__in=serializer.validated_data["points"])
            if not points.exists():
                return Response({"error": "No Points found for provided IDs"}, status=status.HTTP_404_NOT_FOUND)

            intersecting_points = self._find_intersections(points, polygon)
            serializer = PointSerializer(intersecting_points, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer(self, *args, **kwargs):
        return PontIdsSerializer(*args, **kwargs)

    def _find_intersections(self, points, polygon):
        """
        Find points that intersects with the specified polygon.
        This method iterates through the provided points and checks if their locations intersect with the given polygon.
        """
        return [point for point in points.iterator() if point.location.intersects(polygon.polygon)]


class JoinLinesAPIView(APIView):
    """
    A view that joins multiple LineString geometries based on provided IDs and returns the merged result as a GeoJSON.

    Methods:
        - post: Validates input LineString IDs, merges geometries, and returns the result in GeoJSON format.

    """

    allowed_methods = ["post"]

    def post(self, request, format="json"):
        """
        Handles POST request to merge LineString geometries.

        Expects a JSON object with 'lines' key containing list of LineString IDs.

        Returns:
            - 200 OK: Merged LineStrings in GeoJSON format.
            - 400 Bad Request: If input is invalid.
            - 404 Not Found: If no LineStrings are found for provided IDs.
        """
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": "No proper line ids have been provided!"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            line_strings = DBLineString.objects.filter(id__in=serializer.validated_data["lines"])
            if not line_strings.exists():
                return Response({"error": "No LineStrings found for provided IDs"}, status=status.HTTP_404_NOT_FOUND)

            combined_geometry = line_strings.aggregate(union=Union("line"))["union"]
            merged_line = combined_geometry.merged
            geojson_result = json.loads(GEOSGeometry(merged_line.wkt).geojson)

            return Response(geojson_result, status=status.HTTP_200_OK)

    def get_serializer(self, *args, **kwargs):
        return LineStringIdsSerializer(*args, **kwargs)
