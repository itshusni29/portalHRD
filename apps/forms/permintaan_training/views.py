# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TrainingForm, ParticipantFormSet
from ..models import Training, Participant
from django.contrib.auth.decorators import login_required
from django.conf import settings

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

            return redirect('training_list')  # Redirect to training list

    else:
        training_form = TrainingForm()
        participant_formset = ParticipantFormSet(queryset=Participant.objects.none())

    return render(request, 'forms/permintaan_training/Create_permintaan_training.html', {
        'training_form': training_form,
        'participant_formset': participant_formset
    })


def training_list(request):
    trainings = Training.objects.all()  # Get all training requests
    return render(request, 'forms/permintaan_training/permintaan_training.html', {
        'trainings': trainings
    })


