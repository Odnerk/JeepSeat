import json
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
    active_routes = Route.objects.prefetch_related('stops', 'jeeps').all()
    active_jeeps = EJeep.objects.select_related('route', 'tracker', 'next_stop', 'driver').all()
    user_recent_plans = TripPlan.objects.filter(user=request.user).order_by('-created_at')[:3]
    recent_complaints = Complaint.objects.filter(reporter=request.user).order_by('-created_at')[:3]

    # Prepare serialized data for Leaflet Interactive Map
    route_colors = ['#0066cc', '#16a34a', '#d97706', '#9333ea', '#dc2626']
    map_routes = []
    for idx, r in enumerate(active_routes):
        stops_list = [
            {
                'name': s.name,
                'order': s.stop_order,
                'lat': float(s.latitude),
                'lng': float(s.longitude)
            }
            for s in r.stops.order_by('stop_order')
        ]
        map_routes.append({
            'id': r.id,
            'name': r.name,
            'color': route_colors[idx % len(route_colors)],
            'stops': stops_list
        })

    map_jeeps = []
    for j in active_jeeps:
        has_tracker = hasattr(j, 'tracker') and j.tracker and j.tracker.current_lat and j.tracker.current_long
        lat = float(j.tracker.current_lat) if has_tracker else 14.6200
        lng = float(j.tracker.current_long) if has_tracker else 121.0530
        is_online = j.tracker.is_online if has_tracker else False

        map_jeeps.append({
            'id': j.id,
            'plate_number': j.plate_number,
            'route_name': j.route.name if j.route else 'Unassigned',
            'route_id': j.route.id if j.route else None,
            'lat': lat,
            'lng': lng,
            'is_online': is_online,
            'load': j.current_passenger_load,
            'capacity': j.max_capacity,
            'occupancy': f"{j.current_passenger_load}/{j.max_capacity}",
            'next_stop': j.next_stop.name if j.next_stop else 'Terminal Depot',
            'driver': (j.driver.get_full_name() or j.driver.username) if j.driver else 'Unassigned'
        })

    return render(request, 'home.html', {
        'total_routes': total_routes,
        'total_jeeps': total_jeeps,
        'online_trackers': online_trackers,
        'total_seats': total_seats,
        'available_seats': available_seats,
        'active_routes': active_routes[:4],
        'active_jeeps': active_jeeps[:4],
        'user_recent_plans': user_recent_plans,
        'recent_complaints': recent_complaints,
        'map_routes_json': json.dumps(map_routes),
        'map_jeeps_json': json.dumps(map_jeeps),
    })

def auto_login_view(request):
    user = CustomUser.objects.filter(username="maria_santos").first() or CustomUser.objects.first()
    if user:
        login(request, user)
    return redirect(request.GET.get('next', '/'))

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

@login_required
def profile_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        role = request.POST.get('role', '').strip()
        
        user = request.user
        if first_name: user.first_name = first_name
        if last_name: user.last_name = last_name
        if email: user.email = email
        if role in ['commuter', 'conductor', 'driver']: user.role = role
        user.save()
        return redirect('users:profile')

    return render(request, 'users/profile.html', {
        'user': request.user,
    })
