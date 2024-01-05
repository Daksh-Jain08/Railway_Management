from django.urls import path
from . import views as base_views
from users import views as users_views
from trains import views as trains_views
from stations import views as station_views
from tickets import views as tickets_views

urlpatterns = [
    path("", base_views.home, name='home'),
    path("profile/", base_views.profileView, name='profile'),
    path("my_tickets/", base_views.MyTicketsView, name='my-tickets'),
    
    path("register/", users_views.register, name='register'),
    path("login/", users_views.loginUser, name='login'),
    path("logout/", users_views.logoutUser, name='logout'),

    path('create-train/', trains_views.CreateTrain, name='create-train'),

    path('create-station/', station_views.CreateStation, name='create-station'),

    path('book-ticket/', tickets_views.TicketBookingView, name='book-ticket'),
    path('passenger-details/', tickets_views.PassengerDetailsView, name='passenger-details'),
    path('ticket-confirmation/', tickets_views.BookingConfirmationView, name='booking-confirmation')
]
