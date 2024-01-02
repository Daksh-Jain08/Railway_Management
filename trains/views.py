from django.shortcuts import render, redirect
from .forms import TrainCreationForm
from django.contrib import messages


def CreateTrain(request):
    message = None
    if request.method == 'POST':
        form = TrainCreationForm(request.POST)
        if form.is_valid():
            form.save()
            message = messages.success(request, 'Train successfully created')
            return redirect('create-train')
        else:
            message = messages.error(request, 'Error in validating form.')
    form = TrainCreationForm()
    context = {'form': form, 'messsage': message}
    return render(request, 'trains/create_train.html', context)