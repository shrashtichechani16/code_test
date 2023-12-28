import csv
from io import StringIO
from celery import shared_task
from ..models import Student, Parent, AcademicDetails, Document
from datetime import datetime
from django.core.mail import send_mail
from harbie import settings
@shared_task
def process_csv_data(csv_data):
    csv_file = StringIO(csv_data)
    reader = csv.DictReader(csv_file)

    for row in reader:
        dob = datetime.strptime(row['dob'], '%Y-%m-%d').date()
        date_of_joining = datetime.strptime(row['date_of_joining'], '%Y-%m-%d').date()
        student = Student.objects.create(
            name=row['name'],
            gender=row['gender'],
            adhar_card_number=row['adhar_card_number'],
            dob=dob,
            identification_marks=row['identification_marks'],
            category=row['category'],
            height=row['height'],
            weight=row['weight'],
            mail_id=row['mail_id'],
            contact_detail=row['contact_detail'],
            address=row['address'],
        )
        parent = Parent.objects.create(
            father_name=row['father_name'],
            father_qualification=row['father_qualification'],
            father_profession=row['father_profession'],
            father_designation=row['father_designation'],
            father_aadhar_card=row['father_aadhar_card'],
            father_mobile_number=row['father_mobile_number'],
            father_mail_id=row['father_mail_id'],
            mother_name=row['mother_name'],
            mother_qualification=row['mother_qualification'],
            mother_profession=row['mother_profession'],
            mother_designation=row['mother_designation'],
            mother_aadhar_card=row['mother_aadhar_card'],
            mother_mobile_number=row['mother_mobile_number'],
            mother_mail_id=row['mother_mail_id'],
            student=student
        )
        academic_details, created = AcademicDetails.objects.get_or_create(
            student=student,
            defaults={
                'class_name': row['class_name'],
                'section': row['section'],
                'date_of_joining': date_of_joining,
                'session':row['session']
            }
        )

        if not created:
            academic_details.class_name = row['class_name']
            academic_details.section = row['section']
            academic_details.date_of_joining = date_of_joining
            academic_details.save()

    return "CSV data processed successfully."


