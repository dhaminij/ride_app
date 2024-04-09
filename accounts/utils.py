from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunction
from .models import Ride, Driver

def match_ride_to_driver(ride):
    # Get all available drivers
    available_drivers = Driver.objects.filter(is_available=True)

    if not available_drivers:
        # No available drivers, mark the ride as unfulfilled
        ride.status = 'UNFULFILLED'
        ride.save()
        return

    # Calculate distances between the pickup location of the ride and current locations of available drivers
    ride_pickup_location = ride.pickup_location
    for driver in available_drivers:
        distance = driver.current_location.distance(ride_pickup_location)
        if distance <= Distance(km=5):  # Example: match rides within 5 km
            # Assign the driver to the ride and update the ride status
            ride.driver = driver.user
            ride.status = 'ACCEPTED'
            ride.save()
            break
