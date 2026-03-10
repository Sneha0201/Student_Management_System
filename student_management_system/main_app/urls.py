from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="home"), # This makes login page the default
    path("login/", views.login_view, name="login"),
    path("admin-home/", views.admin_home, name="admin_home"),
    path("student-home/", views.student_home, name="student_home"),
    path("staff-home/", views.staff_home, name="staff_home"),
    path("logout/", views.doLogout, name="logout"),
    path("add-staff/", views.add_staff, name="add_staff"),
    path("save-staff", views.save_staff, name="save_staff"),
    path("add-student/", views.add_student, name="add_student"),
    path("save-student/", views.save_student, name="save_student"),
    path("manage-staff/", views.manage_staff, name="manage_staff"),
    path("edit-staff/<int:staff_id>/", views.edit_staff, name="edit_staff"),
    path("update-staff/", views.update_staff, name="update_staff"),
    path("delete-staff/<int:staff_id>/", views.delete_staff, name="delete_staff"),
    path("add-student/", views.add_student, name="add_student"),
    path("manage-student/", views.manage_student, name="manage_student"),
    path("edit-student/<int:student_id>/", views.edit_student, name="edit_student"),
    path("update-student/", views.update_student, name="update_student"),
    path("delete-student/<int:student_id>/", views.delete_student, name="delete_student"),
    path("student-profile/", views.student_profile, name="student_profile"),
    path("staff-profile/", views.staff_profile, name="staff_profile"),
    path("export-students/", views.export_students_csv, name="export_students_csv"),
    path("mark-attendance/<int:student_id>/", views.mark_attendance, name="mark_attendance"),
]