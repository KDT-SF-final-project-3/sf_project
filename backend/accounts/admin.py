from django.contrib import admin
from .models import Employee, CustomUser

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'name', 'team', 'position')
    search_fields = ('emp_no', 'name')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('userID', 'email', 'name', 'position', 'is_approved', 'is_active', 'is_staff', 'last_login')
    search_fields = ('userID', 'email', 'employee__name', 'employee__emp_no')
    list_filter = ('is_approved', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('userID', 'password')}),
        ('개인 정보', {'fields': ('email', 'employee')}),
        ('권한', {'fields': ('is_approved', 'is_active', 'is_staff')}),
        ('중요한 날짜', {'fields': ('last_login',)}),
    )
    readonly_fields = ('last_login',)
    ordering = ('userID',)
    filter_horizontal = ()
    # raw_id_fields = ('employee',) # ForeignKey를 raw ID 필드로 표시 (선택 사항)

    def name(self, obj):
        return obj.employee.name
    name.short_description = '이름'
    name.admin_order_field = 'employee__name'

    def position(self, obj):
        return obj.employee.position
    position.short_description = '직책'
    position.admin_order_field = 'employee__position'

    def save_model(self, request, obj, form, change):
        # 사용자를 생성할 때 비밀번호를 해싱합니다.
        if not obj.pk:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)