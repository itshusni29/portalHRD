from django import forms
from django.contrib.auth import get_user_model
from ..models import Training, GMApproval, ManagerApproval, HRDManagerApproval, TrainingStatus

User = get_user_model()

class TrainingForm(forms.ModelForm):
    requestor_nik = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Training
        fields = [
            'requestor_nik', 'topic', 'background', 'target', 'participants', 
            'trainer', 'date', 'location', 'cost', 'evaluation_level', 
            'manager', 'gm', 'hrd_manager'
        ]
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'background': forms.Textarea(attrs={'class': 'form-control'}),
            'target': forms.TextInput(attrs={'class': 'form-control'}),
            'participants': forms.Textarea(attrs={'class': 'form-control'}),
            'trainer': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'evaluation_level': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'gm': forms.Select(attrs={'class': 'form-control'}),
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

    # Optionally, hide the HRD Manager field from the form
    def clean_hrd_manager(self):
        return User.objects.get(id=8)  # Set HRD Manager ID to 3 by default



class TrainingStatusForm(forms.ModelForm):
    class Meta:
        model = TrainingStatus
        fields = ['status', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }


class ManagerApprovalForm(forms.ModelForm):
    approval_status = forms.ChoiceField(
        choices=[(True, 'Approve'), (False, 'Reject')],
        widget=forms.RadioSelect
    )

    class Meta:
        model = ManagerApproval
        fields = ['approval_status', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class GMApprovalForm(forms.ModelForm):
    approval_status = forms.ChoiceField(
        choices=[(True, 'Approve'), (False, 'Reject')],
        widget=forms.RadioSelect
    )

    class Meta:
        model = GMApproval
        fields = ['approval_status', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class HRDManagerApprovalForm(forms.ModelForm):  # Updated to HRDManagerApprovalForm
    approval_status = forms.ChoiceField(
        choices=[(True, 'Approve'), (False, 'Reject')],
        widget=forms.RadioSelect
    )

    class Meta:
        model = HRDManagerApproval  # Keeping the model as HRDManagerApproval
        fields = ['approval_status', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
