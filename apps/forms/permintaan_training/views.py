# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TrainingForm, GMApprovalForm, ManagerApprovalForm, HRDManagerApprovalForm, TrainingStatusForm
from ..models import Training, GMApproval, ManagerApproval, HRDManagerApproval, TrainingStatus
from django.conf import settings
from django.http import HttpResponse
from apps.user.models import User
import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from django.db.models import Count, Q
from .mappings import MANAGER_MAPPING, GM_MAPPING

    

def is_training_and_development(user):
    return user.section == 'training_development'


def request_training_list(request):
    trainings = Training.objects.all()  # Get all training requests
    return render(request, 'forms/permintaan_training/permintaan_training.html', {
        'trainings': trainings
    })

# ======================================================================================================================
# Views: Untuk mendapatkan detail user pada form request training
# ====================================================================================================================== 
def fetch_user_details(request):
    username = request.GET.get('username')
    print(f"Fetching user details for username: {username}")  # Log the incoming username

    user = User.objects.filter(username=username).first()
    
    if user:
        full_name = f"{user.first_name} {user.last_name}"
        department = user.department
        cc = user.cc
        print(f"User found: {full_name}, Department: {department}, CC: {cc}")  # Log found user details
        return HttpResponse(f"{full_name}|{department}|{cc}")
    
    print("User not found")  # Log when the user is not found
    return HttpResponse("User not found")

logger = logging.getLogger(__name__)

# ======================================================================================================================
# Views: Untuk pengajuan form request training baru oleh user tanpa harus logi
# ======================================================================================================================
def request_training_user(request):
    if request.method == 'POST':
        training_form = TrainingForm(request.POST, request.FILES)

        requestor_username = training_form.data.get('requestor_username')
        requestor = User.objects.filter(username=requestor_username).first()

        if not requestor:
            training_form.add_error('requestor_username', "No user found with this username.")
            logger.error(f"No user found with username: {requestor_username}")
        else:
            if training_form.is_valid():
                try:
                    training = training_form.save(commit=False)
                    training.requestor = requestor
                    
                    # Autofill manager and GM based on requestor's section
                    requestor_section = requestor.section  # Assuming 'section' is an attribute of User

                    # Autofill Manager field
                    manager_username = MANAGER_MAPPING.get(requestor_section)
                    if manager_username:
                        manager = User.objects.filter(username=manager_username).first()
                        if manager:
                            training.manager = manager  # Directly assign the User object

                    # Autofill GM field
                    gm_username = GM_MAPPING.get(requestor_section)
                    if gm_username:
                        gm = User.objects.filter(username=gm_username).first()
                        if gm:
                            training.gm = gm  # Directly assign the User object

                    # Assign HRD Manager directly as it's already managed in the form
                    training.hrd_manager = training_form.cleaned_data.get('hrd_manager')
                    training.pic_trainings = training_form.cleaned_data.get('pic_trainings')  # Ensure this is filled
                    training.save()

                    messages.success(request, "Training request submitted successfully!")
                    logger.info(f"Training request created successfully by {requestor_username}.")
                    return redirect('permintaan_training:request_training_list')

                except Exception as e:
                    logger.error(f"Error saving training request: {e}", exc_info=True)
                    messages.error(request, "An error occurred while saving the training request. Please try again.")
            else:
                logger.warning(f"Training form errors: {training_form.errors}")
                messages.error(request, "Please correct the errors below.")

    else:
        training_form = TrainingForm()
        
    hrd_manager = User.objects.get(username="XN02018")  # HRD Manager is fetched once
    return render(request, 'forms/permintaan_training/user_create_permintaan_training.html', {
        'training_form': training_form,
        'hrd_manager': hrd_manager,
    })


    
    
@login_required
@user_passes_test(is_training_and_development, login_url='login')
def edit_training_request(request, training_id):
    training = get_object_or_404(Training, id=training_id)

    if request.method == 'POST':
        # Pass the existing training instance along with the posted data
        training_form = TrainingForm(request.POST, request.FILES, instance=training)

        if training_form.is_valid():
            try:
                # Save the updated training request
                training_form.save()
                messages.success(request, "Training request updated successfully!")
                logger.info(f"Training request {training_id} updated by {request.user.username}.")
                return redirect('permintaan_training:admin_request_training_list')

            except Exception as e:
                logger.error(f"Error updating training request {training_id}: {e}", exc_info=True)
                messages.error(request, "An error occurred while updating the training request.")
        else:
            logger.warning(f"Form errors while updating: {training_form.errors}")
            messages.error(request, "Please correct the errors below.")

    else:
        # Pre-fill the form with the existing training data
        training_form = TrainingForm(instance=training)

        # Fetch HRD Manager for the hidden input
        hrd_manager = User.objects.get(username="XN02018")  # Ensure this is correct logic
        training_form.fields['hrd_manager'].initial = hrd_manager.id  # Set initial value for the hidden field

    return render(request, 'forms/permintaan_training/admin_permintaan_training_edit.html', {
        'training_form': training_form,
        'training': training,
        'hrd_manager': hrd_manager,  # Pass HRD Manager to the template if needed
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


# ======================================================================================================================
# Views: Menampilkan list form request training pada halaman admin
# ======================================================================================================================
@login_required
@user_passes_test(is_training_and_development, login_url='login')
def admin_request_training_list(request):
    # Fetch all training requests
    trainings = Training.objects.all().select_related('training_status')

    return render(request, 'forms/permintaan_training/admin_permintaan_training.html', {
        'trainings': trainings,
    })

# ======================================================================================================================
# Views: Menampilkan  detail dari form request training pada halaman  admin
# ======================================================================================================================
@login_required
@user_passes_test(is_training_and_development, login_url='login')
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
    # Filter training requests assigned to the logged-in GM, and where the most recent status is 'manager_approved'
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

            # Save training status with GM's approval decision and remarks
            TrainingStatus.objects.create(
                training=training,
                status='gm_approved' if gm_approval.approval_status else 'gm_rejected',
                remarks=gm_approval.remarks
            )

            # Update the training object with the GM approval and save
            training.gm_approval = gm_approval
            training.save()

            # Redirect to GM's training list page
            return redirect('permintaan_training:gm_request_training_list')

    else:
        form = GMApprovalForm()

    return render(request, 'forms/permintaan_training/gm_permintaan_training.html', {
        'trainings': trainings,  # Pass only manager-approved training requests
        'form': form,  # Pass the GM approval form to the template
    })

@login_required
def hrd_training_list(request):
    # Filter training requests where the logged-in user is HRD Manager 
    # and has both statuses: 'gm_approved' and 'ok_analisa'
    
    trainings = Training.objects.filter(
        hrd_manager=request.user
    ).annotate(
        status_count=Count('status__status', filter=Q(status__status__in=['gm_approved', 'ok_analisa']))
    ).filter(
        status_count=2  # Ensure both statuses are present
    )
    
    if request.method == 'POST':
        # Handle form submission for HRD Manager approval
        training_id = request.POST.get('training_id')
        training = get_object_or_404(Training, id=training_id)
        form = HRDManagerApprovalForm(request.POST)

        if form.is_valid():
            hrd_approval = form.save(commit=False)
            hrd_approval.training = training 
            hrd_approval.save()

            # Save training status with HRD's approval decision and remarks
            TrainingStatus.objects.create(
                training=training,
                status='hrd_approved' if hrd_approval.approval_status else 'hrd_rejected',
                remarks=hrd_approval.remarks
            )

            # Display success or error messages based on the HRD decision
            if hrd_approval.approval_status:
                messages.success(request, "Training request approved by HRD.")
            else:
                messages.error(request, "Training request rejected by HRD.")

            # Redirect to HRD's training list page
            return redirect('permintaan_training:hrd_request_training_list')

    else:
        form = HRDManagerApprovalForm()

    return render(request, 'forms/permintaan_training/hrd_permintaan_training.html', {
        'trainings': trainings,  
        'form': form,  
    })




logger = logging.getLogger(__name__)

@login_required
@user_passes_test(is_training_and_development, login_url='login')
def edit_training_request(request, training_id):
    training = get_object_or_404(Training, id=training_id)

    if request.method == 'POST':
        training_form = TrainingForm(request.POST, request.FILES, instance=training)

        if training_form.is_valid():
            try:
                # Save the updated training request
                training_form.save()
                messages.success(request, "Training request updated successfully!")
                logger.info(f"Training request {training_id} updated by {request.user.username}.")
                return redirect('permintaan_training:admin_request_training_list')

            except Exception as e:
                logger.error(f"Error updating training request {training_id}: {e}", exc_info=True)
                messages.error(request, "An error occurred while updating the training request.")
        else:
            logger.warning(f"Form errors while updating: {training_form.errors}")
            messages.error(request, "Please correct the errors below.")

    else:
        # Pre-fill the form with the existing training data
        training_form = TrainingForm(instance=training)

    return render(request, 'forms/permintaan_training/admin_permintaan_training_edit.html', {
        'training_form': training_form,
        'training': training,
    })


def print_training_request(request, training_id):
    training = get_object_or_404(Training, id=training_id)
    return render(request, 'forms/permintaan_training/print_training_request.html', {'training': training})


def internal_training_requests(request):
    trainings = Training.objects.filter(jenis='1')  # '1' for Internal training

    return render(request, 'forms/permintaan_training/admin_permintaan_training_internal.html', {
        'trainings': trainings,
    })
    
def eksternal_training_requests(request):
    trainings = Training.objects.filter(jenis='2')  # '1' for eksternal training

    return render(request, 'forms/permintaan_training/admin_permintaan_training_eksternal.html', {
        'trainings': trainings,
    })
