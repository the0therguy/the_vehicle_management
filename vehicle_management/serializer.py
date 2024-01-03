from rest_framework import serializers
from .models import *


class VehicleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleDetails
        fields = '__all__'


class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleDetails
        fields = ['car_model', 'auction_grade']


class VehicleSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleSeries
        fields = ['name']


class VehicleAvailabilitySerializer(serializers.ModelSerializer):
    port_location = serializers.CharField(write_only=True, required=False)
    shed_number = serializers.CharField(write_only=True, required=False)
    ship_details = serializers.CharField(write_only=True, required=False)
    inhouse_address = serializers.CharField(write_only=True, required=False)
    workshop_address = serializers.CharField(write_only=True, required=False)
    other_details = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = VehicleAvailability
        fields = '__all__'


class VehiclePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiclePrice
        fields = '__all__'


class OtherVehicleItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherVehicleItems
        fields = '__all__'
