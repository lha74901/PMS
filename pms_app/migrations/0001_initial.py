# Generated by Django 5.0.6 on 2024-06-17 14:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('department_class', models.CharField(choices=[('hr', 'Human Resources'), ('finance', 'Finance'), ('it', 'Information Technology'), ('marketing', 'Marketing'), ('sales', 'Sales'), ('operations', 'Operations')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('designation', models.CharField(max_length=100)),
                ('employee_id', models.CharField(max_length=20, unique=True)),
                ('hire_date', models.DateField()),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pms_app.department')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_departments', to='pms_app.employee'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late'), ('on_leave', 'On Leave')], max_length=20)),
                ('check_in_time', models.TimeField(blank=True, null=True)),
                ('check_out_time', models.TimeField(blank=True, null=True)),
                ('work_hours', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_leave', models.BooleanField(default=False)),
                ('leave_type', models.CharField(blank=True, choices=[('sick_leave', 'Sick Leave'), ('vacation', 'Vacation'), ('personal_leave', 'Personal Leave'), ('maternity_leave', 'Maternity Leave'), ('paternity_leave', 'Paternity Leave')], max_length=50, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pms_app.employee')),
            ],
            options={
                'unique_together': {('employee', 'date')},
            },
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deductions', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_payable', models.DecimalField(decimal_places=2, max_digits=10)),
                ('allowances', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bonus', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('overtime_pay', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('net_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('payment_method', models.CharField(blank=True, choices=[('bank_transfer', 'Bank Transfer'), ('cash', 'Cash'), ('cheque', 'Cheque')], max_length=50, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pms_app.employee')),
            ],
            options={
                'unique_together': {('employee', 'month', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(default='', max_length=100)),
                ('previous_rating', models.CharField(default='N/A', max_length=100)),
                ('training_hours', models.IntegerField(default=0)),
                ('overtime_hours', models.IntegerField(default=0)),
                ('absent_days', models.IntegerField(default=0)),
                ('rating_score', models.IntegerField(default=0)),
                ('comments', models.TextField(default='')),
                ('review_period_start', models.DateField()),
                ('review_period_end', models.DateField()),
                ('goals_achieved', models.TextField(blank=True, null=True)),
                ('areas_to_improve', models.TextField(blank=True, null=True)),
                ('employee_feedback', models.TextField(blank=True, null=True)),
                ('is_promotion_recommended', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pms_app.employee')),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_performances', to='pms_app.employee')),
            ],
            options={
                'unique_together': {('employee', 'review_period_start', 'review_period_end')},
            },
        ),
    ]
