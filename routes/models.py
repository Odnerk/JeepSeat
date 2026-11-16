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
