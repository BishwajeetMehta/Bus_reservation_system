from django.db import models
from custom_auth.models import User
# Create your models here.

class bus_agency(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=120)
    phone =models.CharField(max_length=15,unique=True)
    email = models.EmailField(unique= True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to ='images/bus_agencies')
    description = models.TextField()
    added_date = models.DateTimeField(auto_now_add=True)

class bus(models.Model):
    bus_type_choices =[
        ('AC','Ac'),
        ('Non-AC',"Non-AC"),
        ('Sleeper','Sleeper')
    ]

    number = models.CharField(max_length=25,unique= True)
    type = models.CharField(max_length=20,choices=bus_type_choices)
    company = models.ForeignKey(bus_agency, on_delete=models.CASCADE)
    total_seat = models.PositiveIntegerField()
    added_date = models.DateTimeField(auto_now_add=True)

class route(models.Model):
    origin = models.CharField(max_length=250)
    destination = models.CharField(max_length=250)


class trip(models.Model):
    bus = models.ForeignKey(bus, on_delete= models.CASCADE)
    route = models.ForeignKey(route, on_delete= models.CASCADE)
    available_seats = models.PositiveIntegerField()
    trip_date = models.DateField()
    departure_time = models.TimeField()


class booking(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    trip = models.ForeignKey(trip, on_delete= models.CASCADE)
    date = models.DateField()
    total_amount = models.DecimalField(max_digits=5, decimal_places=2,editable=False)
    status = models.CharField(max_length=75, default='Booked')
    seat_number = models.PositiveIntegerField()
   
    


