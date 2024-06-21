from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('rules-and-regulations/', views.rule_and_regulation, name='rule_and_regulation'),
    path('announcements/', views.Company_announcement, name='company_announcement'),

    # Employee URLs
    path('employee/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/list/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employee/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employee/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),

    # Attendance URLs
    path('attendance/create/', views.AttendanceCreateView.as_view(), name='attendance_create'),
    path('attendance/list/', views.AttendanceListView.as_view(), name='attendance_list'),

    # Payroll URLs
    path('payroll/create/', views.PayrollCreateView.as_view(), name='payroll_create'),
    path('payroll/list/', views.PayrollListView.as_view(), name='payroll_list'),
    path('payroll/generate/', views.generate_payroll, name='generate_payroll'),

    # Performance URLs
    path('performance/create/', views.PerformanceCreateView.as_view(), name='performance_create'),
    path('performance/list/', views.PerformanceListView.as_view(), name='performance_list'),

    #Department URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:department_id>/', views.department_detail, name='department_detail'),

]