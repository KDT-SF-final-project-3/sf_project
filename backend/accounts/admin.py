from django.contrib import admin
from django import forms
from .models import CustomUser, Employee

# CustomUser 모델에서 사용할 폼 정의
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['emp_no', 'userID', 'email', 'name', 'position', 'is_active', 'is_staff', 'is_approved']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # emp_no가 선택된 경우 name과 position을 자동으로 채워줍니다.
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

# Employee 모델을 관리하는 Admin 설정
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'name', 'position')  # 직번, 이름, 직책을 보여줍니다.
    search_fields = ('emp_no', 'name', 'position')  # 검색할 수 있는 필드
    list_filter = ('position',)  # 직책별로 필터링할 수 있습니다.

# CustomUser 모델을 관리하는 Admin 설정
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('userID', 'emp_no', 'name', 'position', 'is_approved')
    fields = ('emp_no', 'userID', 'password', 'email', 'is_approved', 'is_active', 'is_staff', 'name', 'position')
    readonly_fields = ('name', 'position')

    def save_model(self, request, obj, form, change):
        if obj.emp_no:
            try:
                employee = Employee.objects.get(emp_no=obj.emp_no)
                obj.name = employee.name
                obj.position = employee.position
            except Employee.DoesNotExist:
                # Employee가 존재하지 않을 경우, name과 position을 비우거나
                # 사용자에게 알림을 줄 수 있습니다. 여기서는 일단 비워둡니다.
                obj.name = ''
                obj.position = ''
        super().save_model(request, obj, form, change)

# 모델 등록
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

