from django.contrib.gis.geos import Point, Polygon
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from geo_api.models import DBPolygon, DBPoint


class PolygonIntersectionApiViewTests(APITestCase):
    def setUp(self):
        self.list_of_points_coords = [
            [0.0, 0.0],
            [1.0, 1.0],
            [2.0, 2.0],
            [3.0, 3.0],
            [0.0, 0.0],
        ]
        self.polygon = DBPolygon.objects.create(polygon=Polygon(self.list_of_points_coords))

        self.point1 = DBPoint.objects.create(location=Point(*self.list_of_points_coords[0]))  # Intersects polygon
        self.point2 = DBPoint.objects.create(location=Point(*self.list_of_points_coords[1]))  # Intersects polygon
        self.point3 = DBPoint.objects.create(location=Point(6, 5))  # Not intersects polygon

        # URL for the view
        self.polygon_url = reverse("polygon-intersection", args=[self.polygon.pk])

    def test_get_not_allowed(self):
        """
        Test should return status 405
        """
        response = self.client.get(self.polygon_url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_when_successful_intersection(self):
        """
        Expected http status: 200
        Expected response: list of Point objects in Geojson format
        """
        data = {"points": [self.point1.id, self.point2.id, self.point3.id]}
        response = self.client.post(self.polygon_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # point1 and point3 should intersect
        self.assertTrue(any(point["id"] == self.point1.id for point in response.data["features"]))
        self.assertTrue(any(point["id"] == self.point2.id for point in response.data["features"]))

    def test_when_invalid_polygon(self):
        """
        Test should return status 404
        """
        invalid_url = reverse("polygon-intersection", args=[self.polygon.id + 1])
        data = {"points": [self.point1.id, self.point2.id]}
        response = self.client.post(invalid_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_when_no_points_found(self):
        """
        Test should return status 404
        """
        data = {"points": [self.polygon.id + 1]}
        response = self.client.post(self.polygon_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "No Points found for provided IDs")

    def test_empty_points_list(self):
        """
        Test should return status 400
        """
        data = {"points": []}
        response = self.client.post(self.polygon_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No proper line ids have been provided!")

    def test_invalid_input_format(self):
        """
        Test should return status 400
        """
        data = {"invalid_key": [self.point1.id]}
        response = self.client.post(self.polygon_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
