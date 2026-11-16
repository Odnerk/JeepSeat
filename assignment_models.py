from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('commuter', 'Commuter'),
        ('conductor', 'Conductor'),
        ('driver', 'Driver'),
    ]
    # Supabase UUID for connecting with Supabase Auth (if used)
    supabase_uid = models.UUIDField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='commuter')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
from django.db import models

class Route(models.Model):
    name = models.CharField(max_length=255)
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    base_fare = models.DecimalField(max_digits=10, decimal_places=2)
    per_km_fare = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    name = models.CharField(max_length=255)
    stop_order = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):
        return f"{self.route.name} - {self.name}"
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
from django.db import models
from users.models import CustomUser
from routes.models import Route, RouteStop

class CommuterPing(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='pings')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

class TripPlan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='trip_plans')
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    total_estimated_fare = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class TripLeg(models.Model):
    plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE, related_name='legs')
    leg_order = models.IntegerField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    start_stop = models.ForeignKey(RouteStop, on_delete=models.CASCADE, related_name='start_legs')
    end_stop = models.ForeignKey(RouteStop, on_delete=models.CASCADE, related_name='end_legs')
    estimated_fare = models.DecimalField(max_digits=10, decimal_places=2)
from django.db import models
from users.models import CustomUser
from vehicles.models import EJeep

class Complaint(models.Model):
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='filed_complaints')
    reported_jeep = models.ForeignKey(EJeep, on_delete=models.SET_NULL, null=True, related_name='complaints')
    reported_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='complaints_received')
    complaint_type = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, default='Pending') # Pending, Investigating, Resolved
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.complaint_type} from {self.reporter.username}"
