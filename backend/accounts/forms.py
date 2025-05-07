# form.py
from django import forms
from .models import CustomUser, Employee

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['emp_no', 'userID', 'email', 'name', 'position', 'is_active', 'is_staff', 'is_approved']
        # name과 position은 emp_no 기반으로 자동 설정되므로 forms에서는 제외하거나 읽기 전용 처리 고려
        # exclude = ['name', 'position'] # 폼에서 name과 position 필드 제외

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.emp_no:
            try:
                # emp_no로 Employee 객체를 조회하여 name과 position을 설정
                employee = Employee.objects.get(emp_no=self.instance.emp_no)
                if 'name' in self.fields:  # 필드가 존재하는지 확인 후 초기값 설정
                    self.fields['name'].initial = employee.name
                if 'position' in self.fields:  # 필드가 존재하는지 확인 후 초기값 설정
                    self.fields['position'].initial = employee.position
                # self.fields['name'].widget.attrs['readonly'] = True # 읽기 전용 처리 예시
                # self.fields['position'].widget.attrs['readonly'] = True # 읽기 전용 처리 예시
            except Employee.DoesNotExist:
                if 'name' in self.fields:
                    self.fields['name'].initial = 'Unknown'
                if 'position' in self.fields:
                    self.fields['position'].initial = 'Unknown'

    def clean(self):
        cleaned_data = super().clean()
        emp_no = cleaned_data.get('emp_no')
        if emp_no:
            try:
                employee = Employee.objects.get(emp_no=emp_no)
                cleaned_data['name'] = employee.name
                cleaned_data['position'] = employee.position
            except Employee.DoesNotExist:
                raise forms.ValidationError(f"Employee with emp_no {emp_no} does not exist.")
        return cleaned_data