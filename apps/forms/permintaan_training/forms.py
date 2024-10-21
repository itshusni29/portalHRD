from django import forms
from django.contrib.auth import get_user_model
from ..models import Training, GMApproval, ManagerApproval, HRDManagerApproval, TrainingStatus

User = get_user_model()

class TrainingForm(forms.ModelForm):
    requestor_username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Training
        fields = [
            'requestor_username', 'topic', 'background', 'participants',
            'trainer', 'date', 'date_end', 'jenis', 'cost', 'evaluation_level',
            'manager', 'gm', 'hrd_manager', 'flyer', 'pic_trainings'
        ]
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'background': forms.Textarea(attrs={'class': 'form-control'}),
            'participants': forms.Textarea(attrs={'class': 'form-control'}),
            'trainer': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control'}),
            'jenis': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'evaluation_level': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'gm': forms.Select(attrs={'class': 'form-control'}),
            'flyer': forms.FileInput(attrs={'class': 'custom-file-input'}),
            'pic_trainings': forms.TextInput(attrs={'class': 'form-control'}),
        }

    flyer = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields['manager'].queryset = User.objects.filter(occupation='manager', is_active=True)
        self.fields['gm'].queryset = User.objects.filter(occupation='general_manager', is_active=True)

    def clean_requestor_username(self):
        username = self.cleaned_data.get('requestor_username')
        if len(username) != 7:
            raise forms.ValidationError("Requestor username must be exactly 7 characters long.")
        return username

    def clean_pic_trainings(self):
        jenis = self.cleaned_data.get('jenis')
        if jenis == '1':  # Internal
            return 'RL20155'
        elif jenis == '2':  # External
            return 'XN09542'
        raise forms.ValidationError("Invalid 'jenis' value.")

    def clean_hrd_manager(self):
        return User.objects.get(id=3)

    def clean_flyer(self):
        flyer = self.cleaned_data.get('flyer')
        if flyer is None:
            return flyer  # Optional field

        valid_extensions = ['pdf']
        ext = flyer.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            raise forms.ValidationError('Only .pdf files are allowed.')

        if flyer.size > 2 * 1024 * 1024:  # 2MB
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
        model = HRDManagerApproval  
        fields = ['approval_status', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
