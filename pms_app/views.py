from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from .models import Employee, Attendance, Payroll, Performance, Department
from django.contrib import messages
from datetime import datetime

def base(request):
    return render(request, 'pms_app/base.html')

def home(request):
    return render(request, 'pms_app/home.html')

def rule_and_regulation(request):
    return render(request, 'pms_app/rule_and_regulation.html')

def Company_announcement(request):
    return render(request, 'pms_app/announcement.html')

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'pms_app/department_list.html', {'departments': departments})

def department_detail(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    employees = Employee.objects.filter(department=department)
    return render(request, 'pms_app/department_detail.html', {'department': department, 'employees': employees})
class EmployeeCreateView(generic.CreateView):
    model = Employee
    fields = '__all__'
    template_name = 'pms_app/employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeListView(generic.ListView):
    model = Employee
    context_object_name = 'employees'

class EmployeeDetailView(generic.DetailView):
    model = Employee
    context_object_name = 'employee'

class EmployeeUpdateView(generic.UpdateView):
    model = Employee
    fields = '__all__'
    template_name = 'pms_app/employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeDeleteView(generic.DeleteView):
    model = Employee
    success_url = reverse_lazy('employee_list')

class AttendanceCreateView(generic.CreateView):
    model = Attendance
    fields = '__all__'
    template_name = 'pms_app/attendance_form.html'
    success_url = reverse_lazy('attendance_list')

class AttendanceListView(generic.ListView):
    model = Attendance
    context_object_name = 'attendance_records'

class PayrollCreateView(generic.CreateView):
    model = Payroll
    fields = ['employee', 'month', 'year', 'basic_salary', 'deductions', 'allowances', 'bonus', 'tax', 'overtime_pay', 'payment_date', 'payment_method']

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Payroll created successfully.')
        return redirect('payroll_list')

class PayrollListView(generic.ListView):
    model = Payroll
    context_object_name = 'payroll_records'

def generate_payroll(request):
    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))

        # Get all active employees
        employees = Employee.objects.filter(is_active=True)

        # Generate payroll for each employee
        for employee in employees:
            # Get the attendance records for the employee in the specified month and year
            attendance_records = Attendance.objects.filter(employee=employee, date__month=month, date__year=year)

            # Calculate the total working days
            total_working_days = attendance_records.filter(status='present').count()

            # Calculate the basic salary based on the employee's salary and working days
            basic_salary = employee.salary * total_working_days / 30  # Assuming a month has 30 days

            # Calculate deductions (you can customize this based on your requirements)
            deductions = 0.1 * basic_salary  # Example: 10% deduction

            # Calculate the total payable amount
            total_payable = basic_salary - deductions

            # Create a new payroll record
            payroll = Payroll(
                employee=employee,
                month=month,
                year=year,
                basic_salary=basic_salary,
                deductions=deductions,
                total_payable=total_payable
            )
            payroll.save()

        messages.success(request, 'Payroll generated successfully.')
        return redirect('payroll_list')

    return render(request, 'pms_app/payroll_generate.html')

class PerformanceCreateView(generic.CreateView):
    model = Performance
    fields = ['employee', 'review_period_start', 'review_period_end', 'department', 'previous_rating', 'training_hours', 'overtime_hours', 'absent_days', 'rating_score', 'comments', 'reviewer', 'goals_achieved', 'areas_to_improve', 'employee_feedback', 'is_promotion_recommended']
    success_url = reverse_lazy('performance_list')

class PerformanceListView(generic.ListView):
    model = Performance
    context_object_name = 'performance_records'