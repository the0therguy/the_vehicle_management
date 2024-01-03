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


class VehicleChassisSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleDetails
        fields = ['chassis_number', 'id']


class VehicleReportDataSerializer(serializers.Serializer):
    chassis_number = serializers.CharField(max_length=100)
    car_model = serializers.CharField(max_length=220)
    model_year = serializers.IntegerField()
    shape = serializers.CharField(max_length=4)
    auction_grade = serializers.CharField(max_length=200)
    package = serializers.CharField()
    color = serializers.CharField(max_length=20)
    mileage = serializers.DecimalField(max_digits=10, decimal_places=2)
    cc = serializers.DecimalField(max_digits=10, decimal_places=2)
    seat_capacity = serializers.IntegerField()
    origin_country = serializers.CharField(max_length=100)
    description = serializers.CharField()
    sale_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    grand_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    vehicle_status = serializers.CharField()
