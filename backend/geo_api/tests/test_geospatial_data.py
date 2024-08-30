from django.contrib.gis.geos import Point as GEOSPoint
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from geo_api.models import Point, DEFAULT_SRID


class PointAPITests(APITestCase):

    def setUp(self):
        self.berlin_coordinates = [12.4924, 41.8902]
        self.warsaw_coordinates = [21.017532, 52.237049]
        self.berlin_point = GEOSPoint(*self.berlin_coordinates)
        self.point = Point.objects.create(
            location=self.berlin_point,
        )
        self.point_url = reverse('point-detail', args=[self.point.id])
        self.list_create_url = reverse('point-list-create')
        self.example_data = {
            "location": {
                "type": "Point",
                "coordinates": self.berlin_coordinates
            }
        }

    def test_create_point(self):
        response = self.client.post(self.list_create_url, self.example_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Point.objects.count(), 2)
        self.assertEqual(Point.objects.get(id=response.data['id']).location, self.berlin_point)

    def test_create_point_with_invalid_data(self):
        self.example_data["location"]["type"] = ""
        response = self.client.post(self.list_create_url, self.example_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Point.objects.count(), 1)

    def test_list_points(self):
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["features"]), 1)

    def test_retrieve_point(self):
        response = self.client.get(self.point_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['geometry']['type'], 'Point')
        self.assertEqual(response.data['geometry']['coordinates'], self.berlin_coordinates)
        self.assertEqual(response.data['geometry']['coordinates'], self.berlin_coordinates)

    def test_update_point(self):
        self.example_data["location"]["coordinates"] = self.warsaw_coordinates
        response = self.client.put(self.point_url, self.example_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.point.refresh_from_db()
        self.assertEqual(self.point.location, GEOSPoint(*self.warsaw_coordinates, srid=DEFAULT_SRID))

    def test_update_point_with_invalid_data(self):
        self.example_data["location"]["type"] = ""
        response = self.client.put(self.point_url, self.example_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.point.refresh_from_db()
        self.assertEqual(self.point.location, GEOSPoint(*self.berlin_coordinates, srid=4326))

    def test_delete_point(self):
        response = self.client.delete(self.point_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Point.objects.count(), 0)
