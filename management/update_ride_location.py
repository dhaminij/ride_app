from django.core.management.base import BaseCommand
from background_task.models import Task
from authentication.models import Ride
from django.contrib.gis.geos import Point
import random

class Command(BaseCommand):
    help = 'Update ride location periodically'

    def handle(self, *args, **options):
        rides = Ride.objects.filter(status='ONGOING')  # Only update ongoing rides
        for ride in rides:
            # Simulate updating the current location by adding random offsets
            if ride.current_location:
                latitude = ride.current_location.y + random.uniform(-0.01, 0.01)
                longitude = ride.current_location.x + random.uniform(-0.01, 0.01)
            else:
                latitude = random.uniform(-90, 90)
                longitude = random.uniform(-180, 180)

            ride.current_location = Point(longitude, latitude)
            ride.save()

            # Schedule the next update for this ride
            Task.objects.create(
                task='ride_tracking.tasks.update_ride_location',
                schedule_type='interval',
                seconds=30,
                args=[ride.pk]
            )
