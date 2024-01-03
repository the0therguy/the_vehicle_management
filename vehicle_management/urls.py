from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name=''),
    path('api/v1/vehicle-details/', VehicleDetailsView.as_view(), name='vehicle-details'),
    path('api/v1/vehicle-model-list/', VehicleModelListView.as_view(), name='vehicle-model-list'),
    path('api/v1/vehicle-series/', VehicleSeriesView.as_view(), name='vehicle-series'),
    path('api/v1/vehicle-availability/', VehicleAvailabilityView.as_view(), name='vehicle-availability'),
]
