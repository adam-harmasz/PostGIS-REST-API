from django.contrib.gis.geos import Point, LineString
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from geo_api.models import DBPoint, DBLineString, DEFAULT_SRID


class PointAPITests(APITestCase):

    def setUp(self):
        self.berlin_coordinates = [12.4924, 41.8902]
        self.warsaw_coordinates = [21.017532, 52.237049]
        self.berlin_point = Point(*self.berlin_coordinates)
        self.point = DBPoint.objects.create(
            location=self.berlin_point,
        )
        self.point_url = reverse("point-detail", args=[self.point.id])
        self.list_create_url = reverse("point-list-create")
        self.data_example = {"location": {"type": "Point", "coordinates": self.berlin_coordinates}}

    def test_create_point(self):
        response = self.client.post(self.list_create_url, self.data_example, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DBPoint.objects.count(), 2)
        self.assertEqual(DBPoint.objects.get(id=response.data["id"]).location, self.berlin_point)

    def test_create_point_with_invalid_data(self):
        self.data_example["location"]["type"] = ""
        response = self.client.post(self.list_create_url, self.data_example, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(DBPoint.objects.count(), 1)

    def test_list_points(self):
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["features"]), 1)

    def test_retrieve_point(self):
        response = self.client.get(self.point_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["geometry"]["type"], "Point")
        self.assertEqual(response.data["geometry"]["coordinates"], self.berlin_coordinates)
        self.assertEqual(response.data["geometry"]["coordinates"], self.berlin_coordinates)

    def test_update_point(self):
        self.data_example["location"]["coordinates"] = self.warsaw_coordinates
        response = self.client.put(self.point_url, self.data_example, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.point.refresh_from_db()
        self.assertEqual(self.point.location, Point(*self.warsaw_coordinates, srid=DEFAULT_SRID))

    def test_update_point_with_invalid_data(self):
        self.data_example["location"]["type"] = ""
        response = self.client.put(self.point_url, self.data_example, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.point.refresh_from_db()
        self.assertEqual(self.point.location, Point(*self.berlin_coordinates, srid=DEFAULT_SRID))

    def test_delete_point(self):
        response = self.client.delete(self.point_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DBPoint.objects.count(), 0)


class LineStringAPITests(APITestCase):
    def setUp(self):
        self.coordinates = [[12.4924, 41.8902], [13.4050, 52.5200]]
        self.data_example = {"name": "New LineString", "line": {"type": "LineString", "coordinates": self.coordinates}}
        self.line_string = DBLineString.objects.create(
            name="Test LineString", line=LineString(tuple(self.coordinates[0]), tuple(self.coordinates[1]))
        )
        self.line_string_url = reverse("linestring-detail", args=[self.line_string.id])
        self.list_create_url = reverse("linestring-list-create")

    def test_create_linestring(self):
        response = self.client.post(self.list_create_url, self.data_example, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DBLineString.objects.count(), 2)
        self.assertEqual(DBLineString.objects.get(id=response.data["id"]).name, "New LineString")

    def test_create_linestring_with_invalid_data(self):
        self.data_example["line"]["type"] = "Point"
        response = self.client.post(self.list_create_url, self.data_example, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(DBLineString.objects.count(), 1)

    def test_list_linestrings(self):
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["features"]), 1)
        self.assertEqual(response.data["features"][0]["properties"]["name"], self.line_string.name)

    def test_retrieve_linestring(self):
        response = self.client.get(self.line_string_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["properties"]["name"], self.line_string.name)

    def test_update_linestring(self):
        self.data_example["name"] = "New name"
        response = self.client.put(self.line_string_url, self.data_example, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.line_string.refresh_from_db()
        self.assertEqual(self.line_string.name, "New name")

    def test_delete_linestring(self):
        response = self.client.delete(self.line_string_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DBLineString.objects.count(), 0)
