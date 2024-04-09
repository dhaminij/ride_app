from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.response import Response
from .models import Ride
from .serializers import RideSerializer
from .utils import match_ride_to_driver
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Ride
from .serializers import RideSerializer
from rest_framework import generics
from .models import Ride
from .serializers import RideSerializer, RideDetailSerializer

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CreateRideView(generics.CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer


class RideDetailView(generics.RetrieveAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideDetailSerializer


class ListRidesView(generics.ListAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer


class UpdateRideStatusView(generics.UpdateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

    def patch(self, request, *args, **kwargs):
        ride = self.get_object()
        status = request.data.get('status')

        if status not in [choice[0] for choice in Ride.STATUS_CHOICES]:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        ride.status = status
        ride.save()
        return Response({'message': 'Ride status updated successfully'})
    

class AcceptRideView(generics.UpdateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

    def patch(self, request, *args, **kwargs):
        ride = self.get_object()
        if ride.status == 'REQUESTED':
            match_ride_to_driver(ride)
            return Response({'message': 'Ride accepted successfully'})
        else:
            return Response({'error': 'Ride is not available for acceptance'})