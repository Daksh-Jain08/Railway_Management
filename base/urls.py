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

    path('create-train/', trains_views.CreateTrain, name='create-train'),
    path('create-train-route/<int:pk>/<int:num_stops>', trains_views.TrainRouteView, name='create-train-route'),
    path('create-train-schedule/<int:pk>/<int:num_stops>/', trains_views.TrainScheduleView, name='create-train-schedule'),
    path('view-train-route/<str:pk>', trains_views.ViewTrainRoute, name='view-train-route'),
    path('all-tickets/train/<str:pk>/', trains_views.AllTicketsTrainView, name='all-tickets-train'),
    path('all-tickets/trainRun/<str:pk>/', trains_views.AllTicketsTrainRunView, name='all-tickets-trainRun'),
    path('download-bookings/', trains_views.ExportFile, name='download-bookings'),
    path('all-trains/', trains_views.AllTrainsView, name='all-trains'),
    path('all-trainRuns/<int:pk>/', trains_views.AllTrainRunsView, name='all-trainRuns'),
    path('edit-train/<str:pk>/', trains_views.EditTrianView, name='edit-train'),
    path('delete-train/<str:pk>/', trains_views.DeleteTrainView, name='delete-train'),
    path('delete-trainRun/<str:pk>/', trains_views.DeleteTrainRunView, name='delete-trainRun'),

    path('create-station/', station_views.CreateStation, name='create-station'),

    path('signup/', users_views.Register, name='signup'),
    path('check-new-user/', users_views.CheckNewUser, name='check-new-user'),

    path('book-ticket/', tickets_views.TicketBookingView, name='book-ticket'),
    path('passenger-details/', tickets_views.PassengerDetailsView, name='passenger-details'),
    path('ticket-confirmation/', tickets_views.BookingConfirmationView, name='booking-confirmation'),
    path('choose-route/', tickets_views.RouteChoosingView, name='choose-route'),
    path('valid-trains/', tickets_views.ValidTrainsView, name='valid-trains'),
]
