from django.urls import path
from . import views as base_views
from users import views as users_views
from trains import views as trains_views

urlpatterns = [
    path("", base_views.home, name='home'),
    
    path("register/", users_views.register, name='register'),
    path("login/", users_views.loginUser, name='login'),
    path("logout/", users_views.logoutUser, name='logout'),

    path('create-train', trains_views.CreateTrain, name='create-train')
]
