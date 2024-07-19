from django.contrib import admin
from .models import bus_agency,bus,route,trip,booking
# Register your models here.

@admin.register(bus_agency)
class bus_agency(admin.ModelAdmin):
    list_display = ('id','location','phone', 'email', 'owner','description', 'photo', 'added_date')

@admin.register(bus)
class bus(admin.ModelAdmin):
    list_display = ('id', 'number', 'type', 'company', 'total_seat', 'added_date') 

@admin.register(route)
class route(admin.ModelAdmin):
    list_display = ('id', 'origin', 'destination')

@admin.register(trip)
class trip(admin.ModelAdmin):
    list_display = ('id', 'bus', 'route', 'available_seats', 'trip_date', 'departure_time')

@admin.register(booking)
class booking(admin.ModelAdmin):
    list_display = ('id', 'user', 'trip', 'date', 'total_amount', 'status', 'seat_number')
