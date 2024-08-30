from django.contrib.gis.geos import LineString
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from geo_api.models import DBLineString


class JoinLinesTestCase(APITestCase):

    def setUp(self):
        self.coordinates = [[0.0, 0.0], [1.0, 1.0]]
        self.coordinates2 = [[1.0, 1.0], [3.0, 3.0]]
        self.coordinates3 = [[22.4924, 41.8902], [23.4050, 52.5200]]
        self.coordinates4 = [[23.4924, 42.8902], [24.4050, 53.5200]]
        # LineStrings below can be merged into LineString
        self.line_string = DBLineString.objects.create(name="LineString1", line=LineString(*self.coordinates))
        self.line_string2 = DBLineString.objects.create(name="LineString2", line=LineString(*self.coordinates2))
        # LineStrings below cannot be merged so MultiLineString will be produced
        self.line_string3 = DBLineString.objects.create(name="LineString1", line=LineString(*self.coordinates3))
        self.line_string4 = DBLineString.objects.create(name="LineString2", line=LineString(*self.coordinates4))
        self.join_lines_url = reverse("join-lines")

    def test_get_not_allowed(self):
        response = self.client.get(self.join_lines_url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_when_no_ids_passed_in_body(self):
        """
        Test should return status 400
        """
        response = self.client.post(self.join_lines_url, data={"lines": []})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_wrong_ids_passed_in_body(self):
        """
        Test should return http status 400
        """
        response = self.client.post(self.join_lines_url, data={"lines": [self.line_string.id + self.line_string2.id]})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_when_wrong_ids_passed_in_body(self):
        """
        Test should return http status 404
        """
        response = self.client.post(self.join_lines_url, data={"lines": [self.line_string.id + self.line_string2.id]})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_when_two_line_strings_which_can_be_merged_into_line_string(self):
        """
        Expected http status: 200
        Expected response: LineString in Geoformat
        """

        # We take only second point from the second ListString as on this point lines should merge into one
        expected_response_data = {"type": "LineString", "coordinates": [*self.coordinates, self.coordinates2[1]]}

        response = self.client.post(self.join_lines_url, data={"lines": [self.line_string.id, self.line_string2.id]})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, expected_response_data)

    def test_when_two_line_strings_which_cannot_be_merged_into_line_string(self):
        """
        Expected http status: 200
        Expected response: MultiLineString in Geoformat
        """

        # We take only second point from the second ListString as on this point lines should merge into one
        expected_response_data = {"type": "MultiLineString", "coordinates": [self.coordinates3, self.coordinates4]}

        response = self.client.post(self.join_lines_url, data={"lines": [self.line_string3.id, self.line_string4.id]})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, expected_response_data)
