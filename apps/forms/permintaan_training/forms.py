# C:\inetpub\wwwroot\NewStructure\apps\forms\permintaan_training\forms.py
from django import forms
from django.forms import modelformset_factory
from django.contrib.auth import get_user_model  # Import this
from ..models import Training, Participant

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['nik', 'name', 'section', 'cc']

# Create a formset for participants
ParticipantFormSet = modelformset_factory(Participant, form=ParticipantForm, extra=1)


User = get_user_model()

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = [
            'requestor', 'topic', 'background', 'target', 'participants',
            'trainer', 'date', 'location', 'cost', 'evaluation_level',
            'monitoring_type', 'monitoring_date', 'manager', 'gm', 'hrd_manager'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'monitoring_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        # Populate the manager and gm fields with users from the User model
        self.fields['manager'].queryset = User.objects.filter(is_active=True)  # Filter as needed
        self.fields['gm'].queryset = User.objects.filter(is_active=True)  # Filter as needed
