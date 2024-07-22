from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import bus_agency,route,trip,booking
from . serializers import BusagencySerializer,RouteSerializer,TripSerializer,BookingSerializer
# Create your views here.

class bus_agencyView(APIView):

    def get(self, request):
        agencies = bus_agency.objects.all()
        serializer = BusagencySerializer(agencies, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class routesView(APIView):
    def get (self,request):
        routes =route.objects.all()
        serializer = RouteSerializer(routes, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class AgencyBasedBusesView(APIView):
    def get(self, request, id):
        buses = trip.objects.filter(bus__company=id)
        if buses.exists():
            serializer = TripSerializer(buses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg': 'Sorry, we are not available today'}, status=status.HTTP_404_NOT_FOUND)
    
class RouteBasedBusesView(APIView):
    def get(self,request,id):
        route_buses = trip.objects.filter(route= id)
        if route_buses.exists():
            serializer = TripSerializer(route_buses,many= True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'msg':'Sorry'},status=status.HTTP_404_NOT_FOUND)
        

ADDITIONAL_CHARGES = {
    'AC': 200,
    'Sleeper': 400,
    'Non-AC': 0,
}


class BookingView(APIView):
   
    def post(self, request):
        seat_numbers = request.data.get('seat_numbers', [])
        user_id = request.data.get('user')
        trip_id = request.data.get('trip')

        if not seat_numbers or not user_id or not trip_id:
            return Response({'msg': 'Required data missing'}, status=status.HTTP_400_BAD_REQUEST)

        trip_instance = trip.objects.get(id=trip_id)

        if trip_instance.available_seats < len(seat_numbers):
            return Response({'msg': 'Not enough seats available'}, status=status.HTTP_400_BAD_REQUEST)

     
         # Calculate total amount for all seats
        base_price = trip_instance.price
        bus_type = trip_instance.bus.type
        additional_charge = ADDITIONAL_CHARGES.get(bus_type, 0)
        total_amount_per_seat = base_price + additional_charge
        total_amount = total_amount_per_seat * len(seat_numbers)

        # Update available seats
        trip_instance.available_seats -= len(seat_numbers)
        trip_instance.save()

        # Create bookings
        bookings = []
        for seat_number in seat_numbers:
            booking_instance = booking.objects.create(
                user_id=user_id,
                trip=trip_instance,
                seat_number=seat_number,
                total_amount=total_amount  
            )
            bookings.append(booking_instance)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)