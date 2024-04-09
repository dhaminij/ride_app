# authentication/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from mydrfproject.accounts.utils import match_ride_to_driver
from .models import Ride, Driver
from django.contrib.gis.geos import Point

class RideModelTestCase(TestCase):
    def test_create_ride(self):
        ride = Ride.objects.create(
            rider_id=1,
            pickup_location=Point(0, 0),
            dropoff_location=Point(1, 1)
        )
        self.assertEqual(Ride.objects.count(), 1)

class DriverModelTestCase(TestCase):
    def test_create_driver(self):
        driver = Driver.objects.create(user_id=1)
        self.assertEqual(Driver.objects.count(), 1)

class RideMatchingAlgorithmTestCase(TestCase):
    def test_match_ride_to_driver(self):
        # Create a ride request
        ride = Ride.objects.create(
            rider_id=1,
            pickup_location=Point(0, 0),
            dropoff_location=Point(1, 1)
        )
        # Create an available driver
        driver = Driver.objects.create(user_id=2, current_location=Point(0.1, 0.1))

        # Test the matching algorithm
        match_ride_to_driver(ride)
        self.assertEqual(ride.status, 'ACCEPTED')
        self.assertEqual(ride.driver_id, driver.user_id)

class RideStatusUpdateTestCase(TestCase):
    def test_ride_status_update(self):
        # Create a ride
        ride = Ride.objects.create(
            rider_id=1,
            pickup_location=Point(0, 0),
            dropoff_location=Point(1, 1)
        )

        # Update ride status
        ride.status = 'ACCEPTED'
        ride.save()

        # Retrieve the updated ride
        updated_ride = Ride.objects.get(pk=ride.pk)

        self.assertEqual(updated_ride.status, 'ACCEPTED')

class DriverAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_driver_accept_ride_request(self):
        # Create a ride request
        ride = Ride.objects.create(
            rider_id=1,
            pickup_location=Point(0, 0),
            dropoff_location=Point(1, 1)
        )
        # Create an available driver
        driver = Driver.objects.create(user_id=2, current_location=Point(0.1, 0.1))

        # Driver accepts the ride request
        response = self.client.patch(reverse('accept_ride', kwargs={'pk': ride.pk}))
        self.assertEqual(response.status_code, 200)

class RideTrackingSimulationTestCase(TestCase):
    def test_update_ride_location(self):
        # Create a ride
        ride = Ride.objects.create(
            rider_id=1,
            pickup_location=Point(0, 0),
            dropoff_location=Point(1, 1)
        )

        # Simulate ride tracking update
        ride.current_location = Point(0.5, 0.5)
        ride.save()

        # Retrieve the updated ride
        updated_ride = Ride.objects.get(pk=ride.pk)

        self.assertEqual(updated_ride.current_location, Point(0.5, 0.5))

class RideAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_ride(self):
        url = reverse('create_ride')
        data = {
            'pickup_location': 'Pickup',
            'dropoff_location': 'Dropoff'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ride.objects.count(), 1)
        self.assertEqual(Ride.objects.get().pickup_location, 'Pickup')

    def test_list_rides(self):
        Ride.objects.create(pickup_location='Pickup', dropoff_location='Dropoff')
        Ride.objects.create(pickup_location='Pickup 2', dropoff_location='Dropoff 2')
        
        url = reverse('list_rides')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_ride(self):
        ride = Ride.objects.create(pickup_location='Pickup', dropoff_location='Dropoff')
        url = reverse('ride_detail', args=[ride.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pickup_location'], 'Pickup')
        self.assertEqual(response.data['dropoff_location'], 'Dropoff')