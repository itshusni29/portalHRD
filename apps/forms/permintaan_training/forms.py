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
            'trainer', 'date', 'jenis', 'cost', 'evaluation_level',
            'manager', 'gm', 'hrd_manager', 'flyer', 'pic_trainings', 'managerTarget'
        ]
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'background': forms.Textarea(attrs={'class': 'form-control'}),
            'participants': forms.Textarea(attrs={'class': 'form-control'}),
            'trainer': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'jenis': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'evaluation_level': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'gm': forms.Select(attrs={'class': 'form-control'}),
            'flyer': forms.FileInput(attrs={'class': 'custom-file-input'}),
            'pic_trainings': forms.HiddenInput(),
            'managerTarget': forms.TextInput(attrs={'class': 'form-control'}),
        }

    flyer = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)

        # Fetch users for GM and Manager fields with full names
        users = User.objects.all()
        user_choices = [(user.id, f"{user.username} - {user.first_name} {user.last_name}") for user in users]
        
        
        # Set the choices for GM and Manager fields
        self.fields['gm'].choices = user_choices
        self.fields['manager'].choices = user_choices
        self.fields['pic_trainings'].queryset = users

        # Set initial values using instance IDs for editing
        if self.instance and self.instance.pk:
            self.initial['gm'] = self.instance.gm_id
            self.initial['manager'] = self.instance.manager_id
            self.initial['pic_trainings'] = self.instance.pic_trainings_id 

        # Set fields to not be required
        self.fields['hrd_manager'].required = False
        self.fields['gm'].required = False
        self.fields['manager'].required = False
        self.fields['pic_trainings'].required = False
        self.fields['managerTarget'].required = False 
        self.fields['trainer'].required = False 
        self.fields['date'].required = False  


    def clean_requestor_username(self):
        username = self.cleaned_data.get('requestor_username')
        if len(username) != 7:
            raise forms.ValidationError("Requestor username must be exactly 7 characters long.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        jenis = cleaned_data.get('jenis')

        # Automatically assign pic_trainings based on jenis
        if jenis == '1':  # Internal
            cleaned_data['pic_trainings'] = User.objects.get(username='RL20155')  
        elif jenis == '2':  # External
            cleaned_data['pic_trainings'] = User.objects.get(username='XN09542') 
        else:
            cleaned_data['pic_trainings'] = None 

        return cleaned_data



    def clean_hrd_manager(self):
        # This is not needed anymore since we handle it in the view
        return self.cleaned_data.get('hrd_manager', User.objects.get(username="XN02018"))  # Default HRD Manager

    def clean_flyer(self):
        flyer = self.cleaned_data.get('flyer')
        if flyer is None:
            return flyer  

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
