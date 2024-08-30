import json

from django.contrib.gis.db.models import Union
from django.contrib.gis.geos import GEOSGeometry
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView, Response

from geo_api.models import DBLineString
from geo_api.serializers.geospatial_data import LineStringIdsSerializer


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
            - 500 Internal Server Error: If merging fails.
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
