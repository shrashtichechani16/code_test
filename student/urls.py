from django.urls import path
from student.controllers.bulk_student import csv_file_upload
from student.controllers.create_student import create_student
from student.controllers.update_student import update_student
from student.controllers.get_student_details import get_student_details
from student.controllers.delete_student import delete_student
urlpatterns = [
    path('csv_file_upload', csv_file_upload, name='csv_file_upload'),
    path('create_student', create_student, name='create_student'),
    path('update_student/<int:student_id>/', update_student, name='update_student'),
    path('get_student_details/<int:student_id>/', get_student_details, name='get_student_details'),
    path('delete_student/<int:student_id>/', delete_student, name='delete_student'),


]
