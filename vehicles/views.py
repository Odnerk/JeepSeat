from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import EJeep, Seat, Tracker

@login_required
def fleet_list(request):
    jeeps = EJeep.objects.select_related('driver', 'conductor', 'route', 'tracker', 'next_stop').prefetch_related('seats').all()
    status_filter = request.GET.get('status')
    
    return render(request, 'vehicles/fleet_list.html', {
        'jeeps': jeeps,
    })

@login_required
def vehicle_detail(request, pk):
    jeep = get_object_or_404(
        EJeep.objects.select_related('driver', 'conductor', 'route', 'tracker', 'next_stop').prefetch_related('seats'),
        pk=pk
    )
    seats = jeep.seats.order_by('seat_number')
    
    # Toggle seat status if conductor/driver or test
    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        if seat_id:
            try:
                seat = seats.get(pk=seat_id)
                seat.status = 'occupied' if seat.status == 'available' else 'available'
                seat.save()
                
                # Update current passenger load
                jeep.current_passenger_load = jeep.seats.filter(status='occupied').count()
                jeep.save()
                return redirect('vehicles:vehicle_detail', pk=pk)
            except Seat.DoesNotExist:
                pass
                
    available_seats_count = seats.filter(status='available').count()

    return render(request, 'vehicles/vehicle_detail.html', {
        'jeep': jeep,
        'seats': seats,
        'available_seats_count': available_seats_count,
    })
