from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from routes.models import Route
from vehicles.models import EJeep, Seat, Tracker
from trips.models import TripPlan, CommuterPing
from feedback.models import Complaint

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    total_routes = Route.objects.count()
    total_jeeps = EJeep.objects.count()
    online_trackers = Tracker.objects.filter(is_online=True).count()
    total_seats = Seat.objects.count()
    available_seats = Seat.objects.filter(status='available').count()
    active_routes = Route.objects.prefetch_related('stops', 'jeeps').all()[:4]
    active_jeeps = EJeep.objects.select_related('route', 'tracker', 'next_stop').all()[:4]
    user_recent_plans = TripPlan.objects.filter(user=request.user).order_by('-created_at')[:3]
    recent_complaints = Complaint.objects.filter(reporter=request.user).order_by('-created_at')[:3]

    return render(request, 'home.html', {
        'total_routes': total_routes,
        'total_jeeps': total_jeeps,
        'online_trackers': online_trackers,
        'total_seats': total_seats,
        'available_seats': available_seats,
        'active_routes': active_routes,
        'active_jeeps': active_jeeps,
        'user_recent_plans': user_recent_plans,
        'recent_complaints': recent_complaints,
    })

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
