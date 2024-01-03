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
