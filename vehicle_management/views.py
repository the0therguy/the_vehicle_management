from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializer import *
from .models import *
from rest_framework import generics


# Create your views here.

class IndexView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class VehicleModelListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = VehicleDetails.objects.all()
    serializer_class = VehicleModelSerializer


class VehicleDetailsView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = VehicleDetails.objects.all()
    serializer_class = VehicleDetailSerializer


class VehicleSeriesView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = VehicleSeries.objects.all()
    serializer_class = VehicleSeriesSerializer


class VehicleAvailabilityView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = VehicleAvailability.objects.all()
    serializer_class = VehicleAvailabilitySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Additional validation based on the status
        status_value = serializer.validated_data.get('availability_status')
        if status_value == 'Port' and (
                not serializer.validated_data.get('port_location') or not serializer.validated_data.get('shed_number')):
            return Response({'error': 'Port Location and Shed Number are required when Status is Port.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif status_value == 'Onship' and not serializer.validated_data.get('ship_details'):
            return Response({'error': 'Ship Details is required when Status is Onship.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif status_value == 'Inhouse' and not serializer.validated_data.get('inhouse_address'):
            return Response({'error': 'In House Address is required when Status is Inhouse.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif status_value == 'Workshop' and not serializer.validated_data.get('workshop_address'):
            return Response({'error': 'Workshop Address is required when Status is Workshop.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif status_value == 'Other' and not serializer.validated_data.get('other_details'):
            return Response({'error': 'Other Details is required when Status is Other.'},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VehicleChassisView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = VehicleDetails.objects.all()
    serializer_class = VehicleChassisSerializer


class VehiclePriceDetailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        items = request.data.pop('items', None)

        # Validate the vehicle data
        vehicle_serializer = VehiclePriceSerializer(data=request.data)
        if not vehicle_serializer.is_valid():
            return Response(vehicle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save the vehicle instance
        vehicle_instance = vehicle_serializer.save()

        # Create OtherVehicleItems instances
        bulk_list = []
        for item in items:
            item['vehicle_price'] = vehicle_instance.id  # Link to the newly created vehicle instance
            item_serializer = OtherVehicleItemsSerializer(data=item)
            if item_serializer.is_valid():
                bulk_list.append(item_serializer.save())
            else:
                # Rollback if any item validation fails
                vehicle_instance.delete()
                return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


class VehicleReportView(APIView):
    def get(self, request):
        # Filtering based on query parameters
        chassis_no = request.query_params.get('chassis_no', '')
        car_model = request.query_params.get('car_model', '')
        model_year = request.query_params.get('model_year', '')
        auction_grade = request.query_params.get('auction_grade', '')
        color = request.query_params.get('color', '')
        vehicle_status = request.query_params.get('vehicle_status', '')

        # Build the filter criteria
        filter_criteria = {}
        if chassis_no:
            filter_criteria['chassis_number__icontains'] = chassis_no
        if car_model:
            filter_criteria['car_model__icontains'] = car_model
        if model_year:
            filter_criteria['model_year'] = model_year
        if auction_grade:
            filter_criteria['auction_grade__icontains'] = auction_grade
        if color:
            filter_criteria['color__icontains'] = color
        if vehicle_status:
            filter_criteria['vehicle_status__icontains'] = vehicle_status

        # Query the database and get only required fields
        queryset = VehicleDetails.objects.filter(**filter_criteria)
        report_data = VehicleReportDataSerializer(queryset, many=True).data

        return Response(report_data, status=status.HTTP_200_OK)
