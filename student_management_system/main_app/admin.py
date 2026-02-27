from django.contrib import admin
from .models import Admin, Staff, Student

admin.site.register(Admin)
admin.site.register(Staff)
admin.site.register(Student)