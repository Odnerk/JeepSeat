from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Complaint
from vehicles.models import EJeep
from django.contrib import messages

@login_required
def complaint_list(request):
    status_filter = request.GET.get('status', '').strip()
    complaints = Complaint.objects.select_related('reporter', 'reported_jeep', 'reported_user').order_by('-created_at')
    
    if status_filter:
        complaints = complaints.filter(status=status_filter)

    jeeps = EJeep.objects.all()

    if request.method == 'POST':
        complaint_type = request.POST.get('complaint_type')
        jeep_id = request.POST.get('jeep_id')
        description = request.POST.get('description')

        if complaint_type and description:
            jeep = EJeep.objects.filter(pk=jeep_id).first() if jeep_id else None
            Complaint.objects.create(
                reporter=request.user,
                reported_jeep=jeep,
                complaint_type=complaint_type,
                description=description,
                status='Pending'
            )
            messages.success(request, "Your incident report / complaint has been lodged with the transit oversight board.")
            return redirect('feedback:complaint_list')

    return render(request, 'feedback/complaint_list.html', {
        'complaints': complaints,
        'jeeps': jeeps,
        'current_status': status_filter,
    })
