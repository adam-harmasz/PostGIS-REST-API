from django.urls import path

from geo_api.api_views.geospatial_data import (
    PointListCreateAPIView,
    PointRetrieveUpdateDestroyAPIView,
    LineStringListCreateAPIView,
    LineStringRetrieveUpdateDestroyAPIView,
    PolygonListCreateAPIView,
    PolygonRetrieveUpdateDestroyAPIView,
)
from geo_api.api_views.join_lines import JoinLinesAPIView

urlpatterns = [
    path("points/", PointListCreateAPIView.as_view(), name="point-list-create"),
    path("points/<int:pk>/", PointRetrieveUpdateDestroyAPIView.as_view(), name="point-detail"),
    path("linestrings/", LineStringListCreateAPIView.as_view(), name="linestring-list-create"),
    path("linestrings/<int:pk>/", LineStringRetrieveUpdateDestroyAPIView.as_view(), name="linestring-detail"),
    path("polygons/", PolygonListCreateAPIView.as_view(), name="polygon-list-create"),
    path("polygons/<int:pk>/", PolygonRetrieveUpdateDestroyAPIView.as_view(), name="polygon-detail"),
    path("join_lines/", JoinLinesAPIView.as_view(), name="join-lines"),
]
