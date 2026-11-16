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
