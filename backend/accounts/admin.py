from django.contrib import admin
from .models import CustomUser, Employee
from .forms import CustomUserForm

# Employee 관리 Admin
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'name', 'position')
    search_fields = ('emp_no', 'name', 'position')
    list_filter = ('position',)

# CustomUser 관리 Admin
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserForm  # 사용자 정의 폼 연결
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
                obj.name = ''
                obj.position = ''
        if not change and obj.password:  # 새로운 사용자 생성 시에만 비밀번호 암호화
            obj.set_password(obj.password)  # 비밀번호 암호화
        super().save_model(request, obj, form, change)

# 등록
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(CustomUser, CustomUserAdmin)