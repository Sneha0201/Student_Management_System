from django.contrib import admin
from .models import Admin,Attendance, Staff, Student

admin.site.register(Admin)
admin.site.register(Attendance)
admin.site.register(Staff)
admin.site.register(Student)