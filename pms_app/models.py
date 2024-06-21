from django.db import models

class Department(models.Model):
    DEPARTMENT_CLASS_CHOICES = [
        ('hr', 'Human Resources'),
        ('finance', 'Finance'),
        ('it', 'Information Technology'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('operations', 'Operations'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_departments')
    department_class = models.CharField(max_length=20, choices=DEPARTMENT_CLASS_CHOICES)

    def __str__(self):
        return self.name

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    designation = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Attendance(models.Model):
    ATTENDANCE_STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('on_leave', 'On Leave'),
    ]

    LEAVE_TYPE_CHOICES = [
        ('sick_leave', 'Sick Leave'),
        ('vacation', 'Vacation'),
        ('personal_leave', 'Personal Leave'),
        ('maternity_leave', 'Maternity Leave'),
        ('paternity_leave', 'Paternity Leave'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS_CHOICES)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    work_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    is_leave = models.BooleanField(default=False)
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES, null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee.name} - {self.date}"

class Payroll(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    total_payable = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')

    def __str__(self):
        return f"{self.employee.name} - {self.month}/{self.year}"

    def save(self, *args, **kwargs):
        self.total_payable = self.basic_salary + self.allowances + self.bonus + self.overtime_pay - self.deductions - self.tax
        self.net_salary = self.total_payable
        super().save(*args, **kwargs)
class Performance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, default='')
    previous_rating = models.CharField(max_length=100, default='N/A')
    training_hours = models.IntegerField(default=0)
    overtime_hours = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)
    rating_score = models.IntegerField(default=0)
    comments = models.TextField(default='')
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    reviewer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='reviewed_performances')
    goals_achieved = models.TextField(null=True, blank=True)
    areas_to_improve = models.TextField(null=True, blank=True)
    employee_feedback = models.TextField(null=True, blank=True)
    is_promotion_recommended = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'review_period_start', 'review_period_end')

    def __str__(self):
        return f"{self.employee.name} - Performance Review ({self.review_period_start} to {self.review_period_end})"