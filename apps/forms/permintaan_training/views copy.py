# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TrainingForm, ParticipantFormSet
from ..models import Training, Participant
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from apps.user.models import User



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



def request_training_user(request):
    if request.method == 'POST':
        training_form = TrainingForm(request.POST)
        participant_formset = ParticipantFormSet(request.POST)

        if training_form.is_valid() and participant_formset.is_valid():
            try:
                # Get requestor by NIK
                requestor_nik = training_form.cleaned_data['requestor_nik']
                requestor = User.objects.filter(nik=requestor_nik).first()
                
                if not requestor:
                    training_form.add_error('requestor_nik', "No user found with this NIK.")
                    return render(request, 'forms/permintaan_training/user_create_permintaan_training.html', {
                        'training_form': training_form,
                        'participant_formset': participant_formset
                    })

                training = training_form.save(commit=False)
                training.requestor = requestor  # Set the requestor from the fetched user
                training.hrd_manager = User.objects.get(id=2)  # Assuming HRD Manager ID is 2
                training.save()

                for participant_form in participant_formset:
                    if participant_form.is_valid():
                        participant = participant_form.save()
                        training.participants.add(participant)

                return redirect('request_training_list')
            except Exception as e:
                print("Error saving training:", e)

    else:
        training_form = TrainingForm()
        participant_formset = ParticipantFormSet(queryset=Participant.objects.none())

    return render(request, 'forms/permintaan_training/user_create_permintaan_training.html', {
        'training_form': training_form,
        'participant_formset': participant_formset
    })



def create_training(request):
    if request.method == 'POST':
        training_form = TrainingForm(request.POST)
        participant_formset = ParticipantFormSet(request.POST)

        if training_form.is_valid() and participant_formset.is_valid():
            # Create and save the training instance
            training = training_form.save(commit=False)
            training.requestor = request.user
            training.manager = request.user  # Assuming the logged-in user is the manager
            training.gm = request.user  # Assuming the logged-in user is the GM
            training.hrd_manager = User.objects.get(id=SPECIFIC_HRD_ID)  # Replace with actual HRD ID
            training.save()

            # Save participants and link them to the training
            for participant_form in participant_formset:
                participant = participant_form.save()
                training.participants.add(participant)  # Link the participant to the training

            return redirect('admin_request_training_list')  # Redirect to training list

    else:
        training_form = TrainingForm()
        participant_formset = ParticipantFormSet(queryset=Participant.objects.none())

    return render(request, 'forms/permintaan_training/Create_permintaan_training.html', {
        'training_form': training_form,
        'participant_formset': participant_formset
    })

