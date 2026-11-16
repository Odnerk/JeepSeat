import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jeepseat.settings')
django.setup()

from users.models import CustomUser
from routes.models import Route, RouteStop
from vehicles.models import EJeep, Tracker, Seat
from trips.models import TripPlan, TripLeg, CommuterPing
from feedback.models import Complaint
from django.utils import timezone
from datetime import timedelta

def seed():
    print("Seeding database...")

    # 1. Users
    driver, _ = CustomUser.objects.get_or_create(
        username="mang_cardo",
        defaults={
            "first_name": "Cardo",
            "last_name": "Dalisay",
            "email": "cardo@jeepseat.ph",
            "role": "driver"
        }
    )
    if not driver.password:
        driver.set_password("password123")
        driver.save()

    conductor, _ = CustomUser.objects.get_or_create(
        username="ben_conductor",
        defaults={
            "first_name": "Ben",
            "last_name": "Reyes",
            "email": "ben@jeepseat.ph",
            "role": "conductor"
        }
    )
    if not conductor.password:
        conductor.set_password("password123")
        conductor.save()

    commuter, _ = CustomUser.objects.get_or_create(
        username="maria_santos",
        defaults={
            "first_name": "Maria",
            "last_name": "Santos",
            "email": "maria@jeepseat.ph",
            "role": "commuter"
        }
    )
    if not commuter.password:
        commuter.set_password("password123")
        commuter.save()

    # 2. Routes & Stops
    r1, _ = Route.objects.get_or_create(
        name="Route 101: Cubao - Antipolo via Marcos Highway",
        defaults={
            "start_point": "Araneta City, Cubao",
            "end_point": "Antipolo Cathedral",
            "base_fare": 15.00,
            "per_km_fare": 2.50
        }
    )

    stops_data_1 = [
        ("Araneta Center Terminal", 1, 14.620000, 121.053000),
        ("Katipunan / Aurora Blvd", 2, 14.628000, 121.072000),
        ("Santolan Station (LRT-2)", 3, 14.622000, 121.085000),
        ("SM City Marikina Junction", 4, 14.625000, 121.096000),
        ("Robinsons Metro East", 5, 14.619000, 121.101000),
        ("Masinag Junction", 6, 14.625000, 121.121000),
        ("Antipolo Cathedral Terminal", 7, 14.587000, 121.176000),
    ]
    for name, order, lat, lon in stops_data_1:
        RouteStop.objects.get_or_create(
            route=r1,
            name=name,
            defaults={"stop_order": order, "latitude": lat, "longitude": lon}
        )

    r2, _ = Route.objects.get_or_create(
        name="Route 202: UP Diliman - Philcoa - Katipunan Loop",
        defaults={
            "start_point": "UP Diliman Quezon Hall",
            "end_point": "Katipunan LRT-2",
            "base_fare": 13.00,
            "per_km_fare": 2.00
        }
    )
    stops_data_2 = [
        ("UP Quezon Hall", 1, 14.654000, 121.066000),
        ("Philcoa Jeepney Terminal", 2, 14.653000, 121.053000),
        ("CP Garcia / Maginhawa", 3, 14.649000, 121.063000),
        ("Ateneo Gate 3", 4, 14.639000, 121.077000),
        ("Katipunan LRT-2 Terminal", 5, 14.632000, 121.073000),
    ]
    for name, order, lat, lon in stops_data_2:
        RouteStop.objects.get_or_create(
            route=r2,
            name=name,
            defaults={"stop_order": order, "latitude": lat, "longitude": lon}
        )

    r3, _ = Route.objects.get_or_create(
        name="Route 303: BGC Market! Market! - Pasig Palengke",
        defaults={
            "start_point": "Market! Market! BGC",
            "end_point": "Pasig Mega Market",
            "base_fare": 16.00,
            "per_km_fare": 2.50
        }
    )
    stops_data_3 = [
        ("Market! Market! Transport Bay", 1, 14.549000, 121.056000),
        ("Kalayaan Flyover", 2, 14.558000, 121.059000),
        ("Buting Junction", 3, 14.561000, 121.068000),
        ("San Joaquin Plaza", 4, 14.555000, 121.074000),
        ("Pasig Mega Market", 5, 14.559000, 121.082000),
    ]
    for name, order, lat, lon in stops_data_3:
        RouteStop.objects.get_or_create(
            route=r3,
            name=name,
            defaults={"stop_order": order, "latitude": lat, "longitude": lon}
        )

    # 3. E-Jeeps & Seats
    stop_r1_3 = RouteStop.objects.filter(route=r1, stop_order=3).first()
    jeep1, _ = EJeep.objects.get_or_create(
        plate_number="NAD-3841",
        defaults={
            "driver": driver,
            "conductor": conductor,
            "route": r1,
            "next_stop": stop_r1_3,
            "next_stop_eta": timezone.now() + timedelta(minutes=7),
            "max_capacity": 16,
            "current_passenger_load": 11,
        }
    )

    Tracker.objects.get_or_create(
        ejeep=jeep1,
        defaults={
            "imei": "864209048392019",
            "sim_number": "+639171234567",
            "current_lat": 14.622500,
            "current_long": 121.083100,
            "last_ping_at": timezone.now(),
            "is_online": True,
        }
    )

    # Populate 16 seats for jeep1
    for s_idx in range(1, 17):
        status = "occupied" if s_idx <= 11 else "available"
        Seat.objects.get_or_create(
            ejeep=jeep1,
            seat_number=f"S{s_idx:02d}",
            defaults={"status": status}
        )

    stop_r2_2 = RouteStop.objects.filter(route=r2, stop_order=2).first()
    jeep2, _ = EJeep.objects.get_or_create(
        plate_number="NBP-9204",
        defaults={
            "driver": driver,
            "conductor": conductor,
            "route": r2,
            "next_stop": stop_r2_2,
            "next_stop_eta": timezone.now() + timedelta(minutes=4),
            "max_capacity": 14,
            "current_passenger_load": 6,
        }
    )
    Tracker.objects.get_or_create(
        ejeep=jeep2,
        defaults={
            "imei": "864209048392020",
            "sim_number": "+639189876543",
            "current_lat": 14.653400,
            "current_long": 121.054200,
            "last_ping_at": timezone.now(),
            "is_online": True,
        }
    )
    for s_idx in range(1, 15):
        status = "occupied" if s_idx <= 6 else "available"
        Seat.objects.get_or_create(
            ejeep=jeep2,
            seat_number=f"S{s_idx:02d}",
            defaults={"status": status}
        )

    # 4. Complaints
    Complaint.objects.get_or_create(
        reporter=commuter,
        reported_jeep=jeep1,
        complaint_type="Airconditioning Issue",
        defaults={
            "description": "Cabin air conditioner was blowing warm air during peak afternoon trip.",
            "status": "Investigating"
        }
    )
    Complaint.objects.get_or_create(
        reporter=commuter,
        reported_jeep=jeep2,
        complaint_type="Overcharging Fare",
        defaults={
            "description": "Charged student commuter full standard fare without applying 20% discount.",
            "status": "Resolved"
        }
    )

    # 5. Trips & Pings
    CommuterPing.objects.get_or_create(
        user=commuter,
        latitude=14.620000,
        longitude=121.053000,
    )

    tp, _ = TripPlan.objects.get_or_create(
        user=commuter,
        origin="Araneta City, Cubao",
        destination="Antipolo Cathedral",
        defaults={
            "total_estimated_fare": 32.50
        }
    )
    TripLeg.objects.get_or_create(
        plan=tp,
        leg_order=1,
        defaults={
            "route": r1,
            "start_stop": stops_data_1[0][0] and RouteStop.objects.filter(route=r1, stop_order=1).first(),
            "end_stop": RouteStop.objects.filter(route=r1, stop_order=7).first(),
            "estimated_fare": 32.50
        }
    )

    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed()
