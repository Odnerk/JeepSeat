from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Route, RouteStop

@login_required
def route_list(request):
    query = request.GET.get('q', '').strip()
    routes = Route.objects.prefetch_related('stops', 'jeeps').all()
    if query:
        routes = routes.filter(name__icontains=query) | routes.filter(start_point__icontains=query) | routes.filter(end_point__icontains=query)
    
    return render(request, 'routes/route_list.html', {
        'routes': routes,
        'query': query,
    })

@login_required
def route_detail(request, pk):
    route = get_object_or_404(Route.objects.prefetch_related('stops', 'jeeps__tracker'), pk=pk)
    stops = route.stops.order_by('stop_order')
    
    origin_id = request.GET.get('origin')
    dest_id = request.GET.get('destination')
    calculated_fare = None
    num_stops = 0

    if origin_id and dest_id:
        try:
            origin_stop = stops.get(pk=origin_id)
            dest_stop = stops.get(pk=dest_id)
            stop_diff = abs(dest_stop.stop_order - origin_stop.stop_order)
            num_stops = stop_diff
            calculated_fare = float(route.base_fare) + max(0, stop_diff - 2) * float(route.per_km_fare) * 1.5
            calculated_fare = round(calculated_fare, 2)
        except RouteStop.DoesNotExist:
            pass

    return render(request, 'routes/route_detail.html', {
        'route': route,
        'stops': stops,
        'origin_id': int(origin_id) if origin_id and origin_id.isdigit() else None,
        'dest_id': int(dest_id) if dest_id and dest_id.isdigit() else None,
        'calculated_fare': calculated_fare,
        'num_stops': num_stops,
    })
