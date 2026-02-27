from django.db import models
from django.contrib.auth.models import User

class Admin(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='admin_profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.admin.username

class Staff(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return self.staff.username

class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    address = models.TextField()
    course = models.CharField(max_length=50)

    def __str__(self):
        return self.student.username