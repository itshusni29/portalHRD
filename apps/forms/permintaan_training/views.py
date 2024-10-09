# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TrainingForm, GMApprovalForm, ManagerApprovalForm, HRDManagerApprovalForm, TrainingStatusForm
from ..models import Training, GMApproval, ManagerApproval, HRDManagerApproval, TrainingStatus
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
def admin_request_training_list(request):
    # Fetch all training requests
    trainings = Training.objects.all().select_related('training_status')

    return render(request, 'forms/permintaan_training/admin_permintaan_training.html', {
        'trainings': trainings,
    })

@login_required
def admin_request_training_view(request, training_id):
    # Get the specific training request by ID
    training = get_object_or_404(Training, id=training_id)

    # Get the current status of the training request
    training_status = training.training_status

    if request.method == 'POST':
        # Handle form submission for status update
        form = TrainingStatusForm(request.POST, instance=training_status)

        if form.is_valid():
            # Save the updated status and remarks
            updated_status = form.save(commit=False)
            updated_status.training = training
            updated_status.save()

            # Display appropriate message based on the new status
            messages.success(request, f"Training status updated to {updated_status.get_status_display()}.")

            # Redirect back to the admin list
            return redirect('permintaan_training:admin_request_training_list')
    else:
        # Prefill the form with the current status
        form = TrainingStatusForm(instance=training_status)

    return render(request, 'forms/permintaan_training/admin_view_permintaan_training.html', {
        'training': training,
        'form': form,
    })

@login_required
def admin_delete_training(request, training_id):
    training = get_object_or_404(Training, id=training_id)

    if request.method == 'POST':
        training.delete()
        messages.success(request, 'Training request deleted successfully!')
        return redirect('permintaan_training:admin_request_training_list')

    return render(request, 'forms/permintaan_training/admin_delete_permintaan_training.html', {'training': training})

    
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

            # Update the training status after manager approval using TrainingStatus model
            training_status = TrainingStatus.objects.create(
                training=training,
                status='manager_approved' if manager_approval.approval_status else 'manager_rejected',
                remarks=manager_approval.remarks
            )

            # Display appropriate messages
            if manager_approval.approval_status:
                messages.success(request, "Training request approved successfully.")
            else:
                messages.error(request, "Training request rejected.")

            # Redirect back to the manager's training list view
            return redirect('permintaan_training:manager_request_training_list')

    else:
        form = ManagerApprovalForm()

    return render(request, 'forms/permintaan_training/manager_permintaan_training.html', {
        'trainings': trainings,
        'form': form,
    })

@login_required
def gm_training_list(request):
    # Filter training requests assigned to the logged-in GM,
    # and where the most recent status is 'manager_approved'
    trainings = Training.objects.filter(
        gm=request.user, 
        status__status='manager_approved'  # Filter by related status model
    )

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
                TrainingStatus.objects.create(training=training, status='gm_approved')  # Approved by GM
            else:
                TrainingStatus.objects.create(training=training, status='gm_rejected')  # Rejected by GM

            training.gm_approval = gm_approval  # Link GM approval to the training
            training.save()

            return redirect('permintaan_training:gm_request_training_list')  # Redirect to the GM training list page

    else:
        form = GMApprovalForm()

    return render(request, 'forms/permintaan_training/gm_permintaan_training.html', {
        'trainings': trainings,  # Pass only manager-approved training requests
        'form': form,  # Pass the GM approval form to the template
    })


@login_required
def hrd_training_list(request):
    # Filter training requests where the logged-in user is HRD Manager
    trainings = Training.objects.filter(hrd_manager=request.user)

    if request.method == 'POST':
        # Handle form submission for HRD Manager approval
        training_id = request.POST.get('training_id')
        training = get_object_or_404(Training, id=training_id)
        form = HRDManagerApprovalForm(request.POST)

        if form.is_valid():
            hrd_approval = form.save(commit=False)
            hrd_approval.training = training  # Link HRD approval to the training
            hrd_approval.save()

            # Update the training status after HRD Manager approval
            if hrd_approval.approval_status:
                training.status = 'hrd_approved'  # HRD approved
                messages.success(request, "Training request approved by HRD.")
            else:
                training.status = 'hrd_rejected'  # HRD rejected
                messages.error(request, "Training request rejected by HRD.")
            training.save()

            return redirect('permintaan_training:hrd_request_training_list')  # Redirect to HRD training list page

    else:
        form = HRDManagerApprovalForm()

    return render(request, 'forms/permintaan_training/hrd_permintaan_training.html', {
        'trainings': trainings,  # Pass the training requests to the template
        'form': form,  # Pass the HRD Manager approval form to the template
    })