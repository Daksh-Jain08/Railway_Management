from django.urls import path, include
from . import views as base_views
from users import views as users_views
from trains import views as trains_views
from stations import views as station_views
from tickets import views as tickets_views

urlpatterns = [
    path("accounts/", include("allauth.urls")),

    path("", base_views.home, name='home'),
    path("profile/", base_views.profileView, name='profile'),
    path("my_tickets/", base_views.MyTicketsView, name='my-tickets'),
    path("add-money/", base_views.MoneyAddingView, name='add-money'),
    path('delete-ticket/<str:pk>/', base_views.TicketCancellingView, name='delete-ticket'),
    path('edit-passenger-details/<str:pk>/', base_views.EditPassengerDetailsView, name='edit-passenger-details'),
    
    path("register/", users_views.register, name='register'),
    path("login/", users_views.loginUser, name='login'),
    path("logout/", users_views.logoutUser, name='logout'),

    path('create-train/', trains_views.CreateTrain, name='create-train'),
    path('create-train-route/<int:pk>/<int:num_stops>', trains_views.TrainRouteView, name='create-train-route'),
    path('create-train-schedule/<int:pk>/<int:num_stops>/', trains_views.TrainScheduleView, name='create-train-schedule'),
    path('view-train-route/<str:pk>', trains_views.ViewTrainRoute, name='view-train-route'),
    path('all-tickets/<str:pk>/', trains_views.AllTicketsView, name='all-tickets'),
    path('all-trains/', trains_views.AllTrainsView, name='all-trains'),
    path('edit-train/<str:pk>/', trains_views.EditTrianView, name='edit-train'),
    path('delete-train/<str:pk>/', trains_views.DeleteTrainView, name='delete-train'),

    path('create-station/', station_views.CreateStation, name='create-station'),

    path('book-ticket/', tickets_views.TicketBookingView, name='book-ticket'),
    path('passenger-details/', tickets_views.PassengerDetailsView, name='passenger-details'),
    path('ticket-confirmation/', tickets_views.BookingConfirmationView, name='booking-confirmation'),
    path('choose-route/', tickets_views.RouteChoosingView, name='choose-route'),
    path('valid-trains/', tickets_views.ValidTrainsView, name='valid-trains'),
]
