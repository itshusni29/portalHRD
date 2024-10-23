from django import forms
from django.contrib.auth import get_user_model
from ..models import Training, GMApproval, ManagerApproval, HRDManagerApproval, TrainingStatus

User = get_user_model()

MANAGER_MAPPING = {
    'assembly': 'XN00205',
    'axle_machining': 'RL10014',
    'big_engine_hc_final_inspection': 'XN01677',
    'casting_machining_hc': 'XN01677',
    'cn_administration': 'XN01044',
    'cost_control': 'XN04142',
    'costing_budgeting': 'XN12315',
    'crank_pe': 'RL04021',
    'crank_shaft_machining': 'XN00382',
    'custom_clearance': 'XN00029',
    'customer_relationship': 'XN00506',
    'delivery_control': 'XN04079',
    'delivery_control_plant_2': 'XN04079',
    'die_casting_wheel_ged_2': 'XN00013',
    'die_casting_wheel_ged_6': 'XN00786',
    'direct_inventory_control': 'RL10020',
    'equipment_control': 'XN01781',
    'fa_control': 'XN12315',
    'forging': 'XN00205',
    'forging_heat_treatment_ga_pe': 'XN08862',
    'fork_cam_shift_ht': 'XN00382',
    'fork_shift_final_inspection': 'XN00382',
    'gear_machining': 'RL10014',
    'general_accounting': 'XN12315',
    'general_affairs': 'XN01352',
    'gravity_wheel_ged_6': 'XN00786',
    'hc_machining_pe': 'XN00257',
    'heat_treatment': 'RL10014',
    'high_pressure_die_casting_pe': 'XN01736',
    'ie_automation': 'XN01781',
    'indirect_inventory_control': 'RL10020',
    'industrial_relations_hr_administration': 'XN02018',
    'inventory_operation_control': 'RL10020',
    'iot': 'XN01781',
    'legal_risk_management': 'XN01352',
    'logistic_control': 'XN00083',
    'low_pressure_die_casting_gravity_pe': 'XN00257',
    'machining_painting_wheel_ged_1': 'XN01056',
    'machining_ga_pe': 'XN08862',
    'machining_wheel_pe': 'XN01736',
    'management_information_system': 'RL10017',
    'manufacturing_center': 'XN00787',
    'medical_welfare': 'XN02018',
    'mold_dies_maintenance': 'XN00787',
    'mold_dies_manufacturing': 'XN00787',
    'mtc_engineering_aluminium': 'XN00586',
    'mtc_engineering_steel': 'XN00586',
    'mtc_engineering_utility': 'XN00586',
    'mtc_operation_1': 'XN00935',
    'mtc_operation_2': 'XN00935',
    'mtc_operation_3': 'XN00935',
    'mtc_operation_utility': 'XN00935',
    'painting_assy_wheel_pe': 'XN01736',
    'pin_weight_cam_shaft_machining': 'XN00382',
    'piston_forging_machining_platting': 'XN01677',
    'piston_pe': 'XN00257',
    'poc_wheel': 'XN04079',
    'process_control': 'XN00382',
    'prod_preparation_aluminium': 'XN01736',
    'prod_preparation_steel': 'XN01781',
    'production_control': 'XN04079',
    'production_control_plant_2': 'XN04079',
    'production_planning_system': 'XN00083',
    'purchase_administration': None,
    'purchase_strategy': None,
    'quality_control_1': 'RL03042',
    'quality_control_2': 'RL03042',
    'quality_control_3': 'RL03042',
    'quality_engineering_aluminium': 'XN01736',
    'quality_engineering_steel': 'XN08862',
    'quality_management_system': 'XN01044',
    'quality_system_calibration': 'XN00506',
    'recruitment_selection': 'XN02018',
    'safety_environment': 'XN01044',
    'shaft_parts_pe': 'RL04021',
    'suppliers_relationship': 'XN00506',
    'taxation': 'XN00029',
    'technical_support_documentation': 'XN01736',
    'tools_jig_maintenance': 'XN00787',
    'tpm': 'XN00023',
    'training_development': 'XN02018',
    'treasury': 'XN00029',
    'workshop_center': 'XN01781',
}


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
        # Populate the queryset for manager and gm
        self.fields['manager'].queryset = User.objects.filter(occupation='manager', is_active=True)
        self.fields['gm'].queryset = User.objects.filter(occupation='general_manager', is_active=True)

        # Auto-fill manager based on requestor_username if it is present
        if 'requestor_username' in self.data:
            requestor_username = self.data['requestor_username'].lower()  # Convert to lowercase for consistency
            if requestor_username in MANAGER_MAPPING:
                self.fields['manager'].initial = MANAGER_MAPPING[requestor_username]  # Set manager username

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
