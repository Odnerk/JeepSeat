from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from routes.models import Route, RouteStop
from .models import TripPlan, TripLeg, CommuterPing
from django.contrib import messages

@login_required
def planner(request):
    routes = Route.objects.prefetch_related('stops').all()
    user_plans = TripPlan.objects.filter(user=request.user).order_by('-created_at')[:5]
    user_pings = CommuterPing.objects.filter(user=request.user).order_by('-timestamp')[:5]

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'plan_trip':
            route_id = request.POST.get('route')
            start_stop_id = request.POST.get('start_stop')
            end_stop_id = request.POST.get('end_stop')
            
            if route_id and start_stop_id and end_stop_id:
                route = Route.objects.get(pk=route_id)
                start_stop = RouteStop.objects.get(pk=start_stop_id)
                end_stop = RouteStop.objects.get(pk=end_stop_id)
                
                diff = abs(end_stop.stop_order - start_stop.stop_order)
                fare = float(route.base_fare) + max(0, diff - 2) * float(route.per_km_fare) * 1.5
                fare = round(fare, 2)
                
                plan = TripPlan.objects.create(
                    user=request.user,
                    origin=start_stop.name,
                    destination=end_stop.name,
                    total_estimated_fare=fare
                )
                TripLeg.objects.create(
                    plan=plan,
                    leg_order=1,
                    route=route,
                    start_stop=start_stop,
                    end_stop=end_stop,
                    estimated_fare=fare
                )
                messages.success(request, f"Trip plan created from {start_stop.name} to {end_stop.name}! Estimated Fare: ₱{fare}")
                return redirect('trips:planner')

        elif action == 'ping_location':
            lat = request.POST.get('lat', 14.620000)
            lng = request.POST.get('lng', 121.053000)
            CommuterPing.objects.create(
                user=request.user,
                latitude=lat,
                longitude=lng
            )
            messages.success(request, "Broadcasted pickup ping to nearby E-Jeep drivers!")
            return redirect('trips:planner')

    return render(request, 'trips/trip_planner.html', {
        'routes': routes,
        'user_plans': user_plans,
        'user_pings': user_pings,
    })
