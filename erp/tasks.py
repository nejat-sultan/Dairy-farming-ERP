# from celery import shared_task
# from datetime import timedelta
# from django.utils import timezone
# from .models import Employee

# @shared_task
# def update_leave_hours(update_type):
#     # Update leave hours when probation ends
#     if update_type == "probation":
#         employees = Employee.objects.filter(
#             probation_end_date__lte=timezone.now(),
#             available_leave_hours=0  # Assuming leave hours are zero during probation
#         )

#         for employee in employees:
#             employee.available_leave_hours = 384  # Initial leave hours
#             employee.save()

#     # Add 16 days worth of hours every year (16 days * 8 hours = 128 hours)
#     elif update_type == "annual":
#         yearly_employees = Employee.objects.filter(
#             hire_date__month=timezone.now().month,
#             hire_date__day=timezone.now().day
#         )

#         for employee in yearly_employees:
#             employee.available_leave_hours += 128  # 16 days
#             employee.save()
