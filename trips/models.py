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
