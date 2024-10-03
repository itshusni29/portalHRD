from django import forms
from django.contrib.auth import get_user_model
from ..models import Training

User = get_user_model()

class TrainingForm(forms.ModelForm):
    requestor_nik = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Training
        fields = [
            'requestor_nik', 'topic', 'background', 'target', 'participants',  # Include participants here
            'trainer', 'date', 'location', 'cost', 'evaluation_level', 
            'monitoring_type', 'monitoring_date', 'manager', 'gm', 'hrd_manager'
        ]
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'background': forms.Textarea(attrs={'class': 'form-control'}),
            'target': forms.TextInput(attrs={'class': 'form-control'}),
            'participants': forms.Textarea(attrs={'class': 'form-control'}),  # Ensure it's included in the widgets
            'trainer': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'evaluation_level': forms.Select(attrs={'class': 'form-control'}),
            'monitoring_type': forms.TextInput(attrs={'class': 'form-control'}),
            'monitoring_date': forms.DateInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'gm': forms.Select(attrs={'class': 'form-control'}),
            'hrd_manager': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields['manager'].queryset = User.objects.filter(occupation='manager', is_active=True)
        self.fields['gm'].queryset = User.objects.filter(occupation='general_manager', is_active=True)

    def clean_requestor_nik(self):
        nik = self.cleaned_data.get('requestor_nik')
        if len(nik) != 7:
            raise forms.ValidationError("Requestor NIK must be exactly 7 characters long.")
        return nik
