from django.urls import path
from .views import register_user, user_login, user_logout
from .views import CreateRideView, RideDetailView, ListRidesView,UpdateRideStatusView, AcceptRideView

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('rides/create/', CreateRideView.as_view(), name='create_ride'),
    path('rides/<int:pk>/', RideDetailView.as_view(), name='ride_detail'),
    path('rides/', ListRidesView.as_view(), name='list_rides'),
    path('rides/<int:pk>/update-status/', UpdateRideStatusView.as_view(), name='update_ride_status'),
     path('rides/<int:pk>/accept/', AcceptRideView.as_view(), name='accept_ride'),
]

