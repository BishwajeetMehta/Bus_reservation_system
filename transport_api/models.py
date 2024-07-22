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

    def __str__(self) -> str:
        return self.name

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

    def __str__(self) -> str:
        return (f"{self.company} - Bus_No: {self.number}")

class route(models.Model):
    origin = models.CharField(max_length=250)
    destination = models.CharField(max_length=250)

    def __str__(self) -> str:
        return (f"{self.origin} - {self.destination}")


class trip(models.Model):
    bus = models.ForeignKey(bus, on_delete= models.CASCADE)
    route = models.ForeignKey(route, on_delete= models.CASCADE)
    available_seats = models.PositiveIntegerField()
    price =  models.DecimalField(max_digits=6, decimal_places=2,default=1000)
    trip_date = models.DateField()
    departure_time = models.TimeField()

    def save(self, *args, **kwargs):
        self.available_seats = self.bus.total_seat
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (f'{self.bus.company} -Bus_No: {self.bus.number} - {self.route}')

class booking(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    trip = models.ForeignKey(trip, on_delete= models.CASCADE)
    date = models.DateField()
    total_amount = models.DecimalField(max_digits=5, decimal_places=2,editable=False)
    status = models.CharField(max_length=75, default='Booked')
    seat_number = models.PositiveIntegerField()
   

    def save(self, *args, **kwargs):
        if self.trip.bus.type == 'AC':
            self.total_amount = self.trip.price + 200
        elif self.trip.bus.type == 'Sleeper':
             self.total_amount = self.trip.price + 400
        else:
             self.total_amount = self.trip.price 
        super().save(*args, **kwargs)
    


