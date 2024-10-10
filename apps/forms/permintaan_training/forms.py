from django import forms
from django.contrib.auth import get_user_model
from ..models import Training, GMApproval, ManagerApproval, HRDManagerApproval, TrainingStatus

User = get_user_model()

class TrainingForm(forms.ModelForm):
    requestor_nik = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Training
        fields = [
            'requestor_nik', 'topic', 'background', 'participants', 
            'trainer', 'date', 'location', 'cost', 'evaluation_level', 
            'manager', 'gm', 'hrd_manager', 'flyer', 'date_end'
        ]
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'background': forms.Textarea(attrs={'class': 'form-control'}),
            'participants': forms.Textarea(attrs={'class': 'form-control'}),
            'trainer': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'evaluation_level': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'gm': forms.Select(attrs={'class': 'form-control'}),
            'flyer': forms.FileInput(attrs={'class': 'custom-file-input'}),
            
        }

    flyer = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields['manager'].queryset = User.objects.filter(occupation='manager', is_active=True)
        self.fields['gm'].queryset = User.objects.filter(occupation='general_manager', is_active=True)

    def clean_requestor_nik(self):
        nik = self.cleaned_data.get('requestor_nik')
        if len(nik) != 7:
            raise forms.ValidationError("Requestor NIK must be exactly 7 characters long.")
        return nik

    def clean_hrd_manager(self):
        return User.objects.get(id=3)
    
    def clean_flyer(self):
        flyer = self.cleaned_data.get('flyer')

        # Allow empty flyer field
        if flyer is None:
            return flyer

        # Validate file extension
        valid_extensions = ['pdf']
        ext = flyer.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            raise forms.ValidationError('Only .pdf files are allowed.')

        # Validate file size (max 2MB)
        if flyer.size > 2 * 1024 * 1024:  # 2 MB
            raise forms.ValidationError('The file size must not exceed 2 MB.')

        return flyer

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
