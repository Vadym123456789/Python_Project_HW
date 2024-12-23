# MyProject3_TernerApp/views.py
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from trainers.models import Trainer  # Correct import

def home(request):
    return HttpResponse("Hello, this is the home page.")

@login_required
def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'users/trainers/trainer_list.html', {'trainers': trainers})

@login_required
def trainer_detail(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    return render(request, 'users/trainers/trainer_detail.html', {'trainer': trainer})

