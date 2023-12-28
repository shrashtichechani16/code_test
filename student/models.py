from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import os
class Student(models.Model):
    GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('OBC', 'OBC'),
        ('SC', 'SC'),
        ('ST', 'ST'),
    ]

    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    adhar_card_number = models.CharField(max_length=12)
    dob = models.DateField()
    identification_marks = models.TextField(null=True,blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    height = models.CharField(max_length=20,null=True,blank=True)
    weight = models.CharField(max_length=20,null=True,blank=True)
    mail_id = models.EmailField()
    contact_detail = models.CharField(max_length=15)
    address = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class Parent(models.Model):
    father_name = models.CharField(max_length=255)
    father_qualification = models.CharField(max_length=255)
    father_profession = models.CharField(max_length=255)
    father_designation = models.CharField(max_length=255)
    father_aadhar_card = models.CharField(max_length=20)
    father_mobile_number = models.CharField(max_length=15)
    father_mail_id = models.EmailField()

    mother_name = models.CharField(max_length=255)
    mother_qualification = models.CharField(max_length=255)
    mother_profession = models.CharField(max_length=255,null=True,blank=True)
    mother_designation = models.CharField(max_length=255,null=True,blank=True)
    mother_aadhar_card = models.CharField(max_length=20)
    mother_mobile_number = models.CharField(max_length=15)
    mother_mail_id = models.EmailField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    student = models.ForeignKey(Student, related_name='parents', on_delete=models.CASCADE)

class AcademicDetails(models.Model):
    student = models.ForeignKey(Student, related_name='academic_details',on_delete=models.CASCADE)
    enrollment_id = models.CharField(max_length=12, unique=True, blank=True)
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    date_of_joining = models.DateField(null=True,blank=True)
    session=models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.enrollment_id:
            name_prefix = self.student.name[:3].upper()
            random_number = format(get_random_string(length=3, allowed_chars='123456789'), '0<3')
            enrollment_date = timezone.now().strftime('%d%m%y')
            self.enrollment_id = f"{enrollment_date}{name_prefix}{random_number}"
        super().save(*args, **kwargs)


def document_upload_path(instance, filename):
    return f"student_documents/{instance.student.name}/{filename}"

class Document(models.Model):
    student = models.ForeignKey(Student, related_name='document', on_delete=models.CASCADE)
    
    certificate = models.FileField(upload_to=document_upload_path, null=True, blank=True)
    aadhaar_card = models.FileField(upload_to=document_upload_path, null=True, blank=True)
    poa = models.FileField(upload_to=document_upload_path, null=True, blank=True)
    poi = models.FileField(upload_to=document_upload_path, null=True, blank=True)
    tc = models.FileField(upload_to=document_upload_path, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
