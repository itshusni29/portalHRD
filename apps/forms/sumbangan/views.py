# apps/forms/sumbangan/views.py

from django.shortcuts import render, redirect
from .forms import SumbanganForm
from apps.forms.models import Sumbangan  # Import the model here

def sumbangan_create(request):
    if request.method == 'POST':
        form = SumbanganForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-all')  # Redirect to a list-all page
    else:
        form = SumbanganForm()
    return render(request, 'forms/sumbangan/create.html', {'form': form})

def sumbangan_list(request):
    sumbangan_entries = Sumbangan.objects.all()
    form = SumbanganForm()
    return render(request, 'forms/sumbangan/index.html', {'sumbangan_entries': sumbangan_entries, 'form': form})
