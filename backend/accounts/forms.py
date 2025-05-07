from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['emp_no', 'userID', 'email', 'name', 'position', 'is_active', 'is_staff', 'is_approved']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.emp_no:
            self.fields['name'].initial = self.instance.emp_no.name
            self.fields['position'].initial = self.instance.emp_no.position

    def clean(self):
        cleaned_data = super().clean()
        emp_no = cleaned_data.get('emp_no')
        if emp_no:
            cleaned_data['name'] = emp_no.name
            cleaned_data['position'] = emp_no.position
        return cleaned_data