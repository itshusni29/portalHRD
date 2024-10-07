# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TrainingForm
from ..models import Training
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from apps.user.models import User
from django.contrib.auth.decorators import login_required
import logging
from django.contrib import messages

def request_training_list(request):
    trainings = Training.objects.all()  # Get all training requests
    return render(request, 'forms/permintaan_training/permintaan_training.html', {
        'trainings': trainings
    })



def admin_request_training_list(request):
    trainings = Training.objects.all()  # Get all training requests
    return render(request, 'forms/permintaan_training/admin_permintaan_training.html', {
        'trainings': trainings
    })

def fetch_user_details(request):
    nik = request.GET.get('nik')
    print(f"Fetching user details for NIK: {nik}")  # Log the incoming NIK

    user = User.objects.filter(nik=nik).first()
    
    if user:
        full_name = f"{user.first_name} {user.last_name}"
        department = user.department
        cc = user.cc
        print(f"User found: {full_name}, Department: {department}, CC: {cc}")  # Log found user details
        return HttpResponse(f"{full_name}|{department}|{cc}")
    
    print("User not found")  # Log when the user is not found
    return HttpResponse("User not found")

logger = logging.getLogger(__name__)
def request_training_user(request):
    if request.method == 'POST':
        training_form = TrainingForm(request.POST)

        requestor_nik = training_form.data.get('requestor_nik')
        requestor = User.objects.filter(nik=requestor_nik).first()

        if not requestor:
            training_form.add_error('requestor_nik', "No user found with this NIK.")
            logger.error(f"No user found with NIK: {requestor_nik}")
        else:
            if training_form.is_valid():
                try:
                    training = training_form.save(commit=False)
                    training.requestor = requestor
                    training.hrd_manager = User.objects.get(id=3)  # Assign HRD Manager
                    training.save()

                    messages.success(request, "Training request submitted successfully!")
                    logger.info(f"Training request created successfully by {requestor_nik}.")
                    return redirect('permintaan_training:request_training_list')

                except Exception as e:
                    logger.error(f"Error saving training request: {e}", exc_info=True)
                    messages.error(request, "An error occurred while saving the training request. Please try again.")
            else:
                logger.warning(f"Training form errors: {training_form.errors}")
                messages.error(request, "Please correct the errors below.")

    else:
        training_form = TrainingForm()

    return render(request, 'forms/permintaan_training/user_create_permintaan_training.html', {
        'training_form': training_form,
    })


def create_training(request):
    if request.method == 'POST':
        training_form = TrainingForm(request.POST)

        if training_form.is_valid():
            # Create and save the training instance
            training = training_form.save(commit=False)
            training.requestor = request.user
            training.manager = request.user  # Assuming the logged-in user is the manager
            training.gm = request.user  # Assuming the logged-in user is the GM
            training.hrd_manager = User.objects.get(id=3)  # Replace with actual HRD ID
            training.save()

            messages.success(request, "Training request created successfully!")
            return redirect('admin_request_training_list')  # Redirect to training list

    else:
        training_form = TrainingForm()

    return render(request, 'forms/permintaan_training/Create_permintaan_training.html', {
        'training_form': training_form,
    })


@login_required
def manager_training_list(request):
    # Filter training requests where the logged-in user is the manager
    trainings = Training.objects.filter(manager=request.user)
    
    return render(request, 'forms/permintaan_training/manager_permintaan_training.html', {
        'trainings': trainings
    })


@login_required
def gm_training_list(request):
    # Filter training requests where the requestor's occupation is 'general_manager' or 'deputy_director'
    if request.user.occupation in ['general_manager', 'deputy_director']:
        trainings = Training.objects.filter(requestor__occupation__in=['general_manager', 'deputy_director'])
    else:
        trainings = Training.objects.none()  # Empty queryset if the user is neither GM nor Deputy Director

    return render(request, 'forms/permintaan_training/gm_permintaan_training.html', {
        'trainings': trainings
    })
