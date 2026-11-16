from django.db import models
from users.models import CustomUser
from routes.models import Route, RouteStop

class EJeep(models.Model):
    driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='driven_jeeps')
    conductor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='managed_jeeps')
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, related_name='jeeps')
    next_stop = models.ForeignKey(RouteStop, on_delete=models.SET_NULL, null=True)
    next_stop_eta = models.DateTimeField(null=True, blank=True)
    plate_number = models.CharField(max_length=20, unique=True)
    max_capacity = models.IntegerField()
    current_passenger_load = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.plate_number

class Tracker(models.Model):
    ejeep = models.OneToOneField(EJeep, on_delete=models.CASCADE, related_name='tracker')
    imei = models.CharField(max_length=50, unique=True)
    sim_number = models.CharField(max_length=20)
    current_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    current_long = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    last_ping_at = models.DateTimeField(null=True)
    is_online = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Tracker for {self.ejeep.plate_number}"

class Seat(models.Model):
    ejeep = models.ForeignKey(EJeep, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    status = models.CharField(max_length=50) # e.g., 'available', 'occupied'
    
    def __str__(self):
        return f"Seat {self.seat_number} - {self.ejeep.plate_number}"
