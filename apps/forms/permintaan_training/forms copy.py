from django import forms
from django.contrib.auth import get_user_model
from ..models import Training, GMApproval, ManagerApproval, HRDManagerApproval, TrainingStatus

User = get_user_model()

GM_MAPPING = {
    'crank_shaft_machining': 'iioyoshimasa',
    'pin_weight_cam_shaft_machining': 'iioyoshimasa',
    'die_casting_wheel_ged_6': 'iioyoshimasa',
    'gravity_wheel_ged_6': 'iioyoshimasa',
    'fork_cam_shift_ht': 'iioyoshimasa',
    'fork_shift_final_inspection': 'iioyoshimasa',
    'process_control': 'iioyoshimasa',
    'tpm': 'iioyoshimasa',
    'prod_preparation_aluminium': 'kenjishimioke',
    'technical_support_documentation': 'kenjishimioke',
    'prod_preparation_steel': 'kenjishimioke',
    'hc_machining_pe': 'kenjishimioke',
    'low_pressure_die_casting_gravity_pe': 'kenjishimioke',
    'piston_pe': 'kenjishimioke',
    'high_pressure_die_casting_pe': 'kenjishimioke',
    'machining_wheel_pe': 'kenjishimioke',
    'painting_assy_wheel_pe': 'kenjishimioke',
    'forging_heat_treatment_ga_pe': 'kenjishimioke',
    'machining_ga_pe': 'kenjishimioke',
    'crank_pe': 'kenjishimioke',
    'shaft_parts_pe': 'kenjishimioke',
    'quality_engineering_steel': 'kenjishimioke',
    'quality_engineering_aluminium': 'kenjishimioke',
    'mtc_engineering_aluminium': 'kurodayohiyuki',
    'mtc_engineering_steel': 'kurodayohiyuki',
    'mtc_engineering_utility': 'kurodayohiyuki',
    'mtc_operation_1': 'kurodayohiyuki',
    'mtc_operation_2': 'kurodayohiyuki',
    'mtc_operation_3': 'kurodayohiyuki',
    'mtc_operation_utility': 'kurodayohiyuki',
    'cn_administration': 'kurodayohiyuki',
    'quality_management_system': 'kurodayohiyuki',
    'safety_environment': 'kurodayohiyuki',
    'axle_machining': 'mizunofumihiro',
    'gear_machining': 'mizunofumihiro',
    'heat_treatment': 'mizunofumihiro',
    'assembly': 'mizunofumihiro',
    'forging': 'mizunofumihiro',
    'big_engine_hc_final_inspection': 'mizunofumihiro',
    'casting_machining_hc': 'mizunofumihiro',
    'piston_forging_machining_platting': 'mizunofumihiro',
    'die_casting_wheel_ged_2': 'XN00013',
    'machining_painting_wheel_ged_1': 'XN00013',
    'fa_control': 'XN00029',
    'general_accounting': 'XN00029',
    'cost_control': 'XN00029',
    'custom_clearance': 'XN00029',
    'taxation': 'XN00029',
    'treasury': 'XN00029',
    'general_affairs': 'XN00029',
    'legal_risk_management': 'XN00029',
    'industrial_relations_hr_administration': 'XN00029',
    'medical_welfare': 'XN00029',
    'management_information_system': 'XN00029',
    'recruitment_selection': 'XN00029',
    'training_development': 'XN00029',
    'costing_budgeting': 'XN00029',
    'direct_inventory_control': 'XN00083',
    'indirect_inventory_control': 'XN00083',
    'inventory_operation_control': 'XN00083',
    'delivery_control': 'XN00083',
    'delivery_control_plant_2': 'XN00083',
    'poc_wheel': 'XN00083',
    'production_control': 'XN00083',
    'production_control_plant_2': 'XN00083',
    'logistic_control': 'XN00083',
    'production_planning_system': 'XN00083',
    'customer_relationship': 'XN00083',
    'quality_system_calibration': 'XN00083',
    'suppliers_relationship': 'XN00083',
    'quality_control_1': 'XN00083',
    'quality_control_2': 'XN00083',
    'quality_control_3': 'XN00083',
    'manufacturing_center': 'XN00786',
    'mold_dies_maintenance': 'XN00786',
    'mold_dies_manufacturing': 'XN00786',
    'tools_jig_maintenance': 'XN00786',
    'equipment_control': 'XN00786',
    'ie_automation': 'XN00786',
    'iot': 'XN00786',
    'workshop_center': 'XN00786',
    'purchase_administration': 'yoshioyamada',
    'purchase_strategy': 'yoshioyamada'
}


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
            'manager': forms.HiddenInput(),  # Hide Manager field
            'gm': forms.HiddenInput(),  # Hide GM field
            'flyer': forms.FileInput(attrs={'class': 'custom-file-input'}),
            'pic_trainings': forms.TextInput(attrs={'class': 'form-control'}),
        }

    flyer = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)

        # Set fields to not be required, since they are autofilled
        self.fields['manager'].required = False
        self.fields['gm'].required = False

        # Autofill manager and GM based on requestor_section from self.data
        requestor_section = self.data.get('requestor_section')

        if requestor_section and requestor_section in MANAGER_MAPPING:
            manager_username = MANAGER_MAPPING.get(requestor_section)
            manager = User.objects.filter(username=manager_username).first()
            if manager:
                self.fields['manager'].initial = manager.id

        if requestor_section and requestor_section in GM_MAPPING:
            gm_username = GM_MAPPING.get(requestor_section)
            gm = User.objects.filter(username=gm_username).first()
            if gm:
                self.fields['gm'].initial = gm.id

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
