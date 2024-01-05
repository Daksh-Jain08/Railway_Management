from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket
from .models import Profile

# Create your views here.

@login_required
def home(request):
    user = request.user
    is_customer = user.is_customer
    is_staff = user.is_staff
    context = {'is_customer': is_customer, 'is_staff': is_staff}
    return render(request, 'base/home.html', context)

@login_required
def profileView(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    tickets_count = tickets.count()
    profile = Profile.objects.get(user=user)
    wallet = profile.wallet
    context = {'username': user.username, 'tickets_count': tickets_count, 'wallet': wallet}
    return render(request, 'base/profile.html', context)

@login_required
def MyTicketsView(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    context = {'tickets': tickets}
    return render(request, 'base/my_tickets.html', context)