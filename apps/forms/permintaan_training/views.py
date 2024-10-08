# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TrainingForm, GMApprovalForm, ManagerApprovalForm
from ..models import Training, GMApproval, ManagerApproval
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from apps.user.models import User
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

    if request.method == 'POST':
        # Handle form submission for manager approval
        training_id = request.POST.get('training_id')
        training = get_object_or_404(Training, id=training_id)
        form = ManagerApprovalForm(request.POST)

        if form.is_valid():
            # Save the manager approval decision
            manager_approval = form.save(commit=False)
            manager_approval.training = training
            manager_approval.save()

            # Update the training status after manager approval
            if manager_approval.approval_status:
                training.status = 'manager_approved'
                messages.success(request, "Training request approved.")
            else:
                training.status = 'manager_rejected'
                messages.error(request, "Training request rejected.")
            training.save()

            return redirect('permintaan_training:manager_request_training_list')

    else:
        form = ManagerApprovalForm()

    return render(request, 'forms/permintaan_training/manager_permintaan_training.html', {
        'trainings': trainings,
        'form': form,
    })



@login_required
def gm_training_list(request):
    # Filter training requests assigned to the logged-in GM
    trainings = Training.objects.filter(gm=request.user)

    if request.method == 'POST':
        # Handle form submission for GM approval
        training_id = request.POST.get('training_id')
        training = get_object_or_404(Training, id=training_id)
        form = GMApprovalForm(request.POST)

        if form.is_valid():
            gm_approval = form.save(commit=False)
            gm_approval.training = training  # Link the GM approval to the training
            gm_approval.save()

            # Update the training status based on the GM's approval
            if gm_approval.approval_status:
                training.status = 'gm_approved'  # Approved by GM
            else:
                training.status = 'gm_rejected'  # Rejected by GM
            training.gm_approval = gm_approval  # Link GM approval to the training
            training.save()

            return redirect('permintaan_training:gm_request_training_list')  # Redirect to the GM training list page

    else:
        form = GMApprovalForm()

    return render(request, 'forms/permintaan_training/gm_permintaan_training.html', {
        'trainings': trainings,  # Pass the training requests to the template
        'form': form,  # Pass the GM approval form to the template
    })
