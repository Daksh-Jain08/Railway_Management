from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tickets.models import Ticket
from .models import Profile
from .forms import MoneyAddingForm

# Create your views here.

@login_required(login_url='/login')
def home(request):
    user = request.user
    is_customer = user.is_customer
    is_staff = user.is_staff
    context = {'is_customer': is_customer, 'is_staff': is_staff}
    return render(request, 'base/home.html', context)

@login_required(login_url='/login')
def profileView(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    tickets_count = tickets.count()
    profile = Profile.objects.get(user=user)
    wallet = profile.wallet
    context = {'username': user.username, 'tickets_count': tickets_count, 'wallet': wallet}
    return render(request, 'base/profile.html', context)

@login_required(login_url='/login')
def MyTicketsView(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    context = {'tickets': tickets}
    return render(request, 'base/my_tickets.html', context)

@login_required(login_url='/login')
def MoneyAddingView(request):
    message = None
    if request.method == 'POST':
        form = MoneyAddingForm(request.POST)
        if form.is_valid():
            money = form.cleaned_data.get('money')
            profile = Profile.objects.get(user=request.user)
            profile.wallet += money
            profile.save()

        else:
            message = messages.error(request, "Error validating Form!")
    
    form = MoneyAddingForm()
    context = {'form': form, 'message': message}
    return render(request, 'base/money_add.html', context)


@login_required(login_url='/login')
def TicketDeletingView(request, pk):
    ticket = Ticket.objects.get(id=pk)
    user = ticket.user
    profile = Profile.objects.get(user=user)
    train = ticket.train
    fare = train.fare

    if request.user != ticket.user:
        message = messages.warning(request, "What are you trying to do? You are not allowed to do this!!")

    if request.method == 'POST':
        ticket.delete()
        profile.wallet += fare
        profile.save()
        message = messages.success(request, "Ticket has been canceled successfully. Money has been refunded.")
        return redirect('my-tickets')
    
    return render(request, 'base/delete.html', {'obj': ticket})