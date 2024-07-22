from rest_framework import serializers
from .models import bus,trip,bus_agency,route,booking

class BusagencySerializer(serializers.ModelSerializer):
    class Meta:
        model = bus_agency
        fields ='__all__'

class BusSerializer(serializers.ModelSerializer):
    company = BusagencySerializer()
    class Meta:
        model = bus
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = route
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
   bus = BusSerializer ()
   route = RouteSerializer()
   class Meta:
       model= trip
       fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = booking
        fields = '__all__'
   

