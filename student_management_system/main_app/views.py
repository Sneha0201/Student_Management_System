import csv 
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from main_app.models import Staff, Student
from .models import Attendance, Student, Staff

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("admin_home")
            elif hasattr(user, 'staff'):
                return redirect("staff_home")
            elif hasattr(user, 'student'):
                return redirect("student_home")
        else:
            return render(request, "main_app/login.html", {"error": "Invalid credentials"})
    return render(request, "main_app/login.html")

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_superuser:
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required(login_url="login")
def admin_home(request):
    total_staff = Staff.objects.count()
    total_student = Student.objects.count()
    total_admin = User.objects.filter(is_superuser=True).count()
    context = {
        "total_staff": total_staff,
        "total_student": total_student,
        "total_admin": total_admin,
    }
    return render(request, "main_app/admin_home.html", context)

@login_required(login_url="login")
def student_home(request):
    return render(request, "main_app/student_home.html")

@login_required(login_url="login")
def staff_home(request):
    staff = Staff.objects.get(staff=request.user)
    students = Student.objects.filter(staff=staff)
    return render(request, "main_app/staff_home.html", {"students": students})

def doLogout(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
@admin_required
def add_staff(request):
    return render(request, "main_app/add_staff.html")

def save_staff(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        address = request.POST.get("address")
        user = User.objects.create_user(username=username, password=password)
        Staff.objects.create(staff=user, address=address)
        return redirect("admin_home")
    else:
        return redirect("add_staff")

@login_required(login_url="login")
@admin_required
def add_student(request):
    staff_list = Staff.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        staff_id = request.POST["staff"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        course = request.POST["course"]
        user = User.objects.create_user(username=username, password=password)
        staff = Staff.objects.get(id=staff_id)
        Student.objects.create(student=user, staff=staff, gender=gender, address=address, course=course)
        return redirect("admin_home")
    return render(request, "main_app/add_student.html", {"staff_list": staff_list})

def save_student(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        course = request.POST.get("course")
        user = User.objects.create_user(username=username, password=password)
        Student.objects.create(
            student=user,
            gender=gender,
            address=address, course=course
        )
        return redirect("admin_home")
    else:
        return redirect("add_student")

@login_required(login_url="login")
@admin_required
def manage_staff(request):
    staff_list = Staff.objects.all()
    return render(request, "main_app/manage_staff.html", {"staff_list": staff_list})

def edit_staff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    if request.method == "POST":
        staff.address = request.POST.get("address")
        staff.save()
        return redirect("manage_staff")
    return render(request, "main_app/edit_staff.html", {"staff":staff})

def update_staff(request):
    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        address = request.POST.get("address")
        staff = Staff.objects.get(id=staff_id)
        staff.address = address
        staff.save()
        return redirect("manage_staff")

def delete_staff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    staff.user.delete()
    staff.delete() # This deletes both User + Staff model
    return redirect("manage_staff")

@login_required(login_url="login")
@admin_required
def manage_student(request):
    query = request.GET.get('q')
    course = request.GET.get('course')
    students = Student.objects.all()
    if query:
        students = students.filter(student__username__icontains=query)
    if course:
        students = students.filter(course__icontains=course)
    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"students": page_obj}
    return render(request, "main_app/manage_student.html", context)

def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)
    staff_list = Staff.objects.all()
    return render(request, "main_app/edit_student.html", {"student": student, "staff_list": staff_list})

def update_student(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        staff_id = request.POST.get("staff")
        course = request.POST.get("course")
        address = request.POST.get("address")
        student = Student.objects.get(id=student_id)
        student.staff = Staff.objects.get(id=staff_id)
        student.course = course
        student.address = address
        student.save()
        return redirect("manage_student")

def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    student.student.delete() # deletes user
    student.delete()
    return redirect("manage_student")

@login_required(login_url="login")
def student_profile(request):
    student = Student.objects.get(student=request.user)
    context = {"student": student}
    return render(request, "main_app/student_profile.html", context)

@login_required(login_url="login")
def staff_profile(request):
    staff = Staff.objects.get(staff = request.user)
    students = Student.objects.filter(staff=staff)
    context = {
        "staff": staff,
        "students": students,
        "student_count": students.count()
    }
    return render(request, "main_app/staff_profile.html", context)

def export_students_csv(request):
    response = HttpResponse(content_type = 'test/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    writer = csv.writer(response)
    writer.writerow(['Username', 'Course', 'Gender', 'Address', 'Staff'])
    students = Student.objects.all()
    for student in students:
        writer.writerow([
            student.student.username,
            student.course,
            student.gender,
            student.address,
            student.staff.staff.username
        ])
    return response

def mark_attendance(request, student_id):
    student = Student.objects.get(id=student_id)
    Attendance.objects.create(
        student=student,
        date=date.today(),
        status=True
    )
    return redirect("manage_student")