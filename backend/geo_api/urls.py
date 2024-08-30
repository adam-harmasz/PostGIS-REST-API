from django.urls import path

from geo_api.api_views.geospatial_data import PointListCreateAPIView, PointRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('points/', PointListCreateAPIView.as_view(), name='point-list-create'),
    path('points/<int:pk>/', PointRetrieveUpdateDestroyAPIView.as_view(), name='point-detail'),
]
