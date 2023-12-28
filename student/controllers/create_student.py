from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from student.models import Student, Parent, AcademicDetails, Document
from rest_framework.response import Response
from datetime import datetime
from harbie import settings
from django.core.mail import send_mail


def send_student_mail(student, academic_details):
    subject = f"Welcome to Dummy School, {student.name}!"
    message = f"Dear {student.name},\nYou are enrolled in Dummy School. Your Enrollment ID is {academic_details.enrollment_id}. Provide us with the required documents for future references.\n\nTeam Dummy School"
    sender = settings.EMAIL_HOST_USER
    send_mail(subject, message, sender, [student.mail_id])

def send_admin_notification(student, academic_details):
    subject = f"New Enrollment at Dummy School"
    message = f"Dear Admin,\nNew student {student.name} enrolled in class {academic_details.class_name}, section {academic_details.section} with enrollment ID {academic_details.enrollment_id} in {academic_details.session} session."
    sender = settings.EMAIL_HOST_USER
    admin_email = 'durganand.jha@habrie.com'  
    send_mail(subject, message, sender, [admin_email])

@api_view(['POST'])
def create_student(request):
    try:

        name = request.data['name']
        gender = request.data['gender']
        adhar_card_number = request.data['adhar_card_number']
        dob = request.data['dob']if 'dob' in request.data else ""
        identification_marks = request.data['identification_marks']if 'identification_marks' in request.data else ""
        category = request.data['category']
        height = request.data['height']if 'height' in request.data else ""
        weight = request.data['weight']if 'weight' in request.data else ""
        mail_id = request.data['mail_id']
        contact_detail = request.data['contact_detail']
        address = request.data['address']
        father_name=request.data['father_name']
        father_qualification=request.data['father_qualification']
        father_profession=request.data['father_profession']
        father_designation= request.data['father_designation']
        father_aadhar_card=request.data['father_aadhar_card']
        father_mobile_number= request.data['father_mobile_number']
        father_mail_id= request.data['father_mail_id']
        mother_name=request.data['mother_name']
        mother_qualification= request.data['mother_qualification']
        mother_profession=request.data['mother_profession']if 'mother_profession' in request.data else ""
        mother_designation= request.data['mother_designation']if 'mother_designation' in request.data else ""
        mother_aadhar_card= request.data['mother_aadhar_card']
        mother_mobile_number= request.data['mother_mobile_number']
        mother_mail_id= request.data['mother_mail_id']
        certificate = request.FILES['certificate']if 'certificate' in request.data else None
        aadhaar_card = request.FILES['aadhaar_card']if 'aadhaar_card' in request.data else None
        poa = request.FILES['poa']if 'poa' in request.data else None
        poi = request.FILES['poi']if 'poi' in request.data else None
        tc = request.FILES['tc']if 'tc' in request.data else None
        allowed_image_types = ["image/jpeg", "image/png", "image/jpg","application/pdf", "application/msword"]
        if certificate and certificate.content_type not in allowed_image_types:
            return Response({"message": "Invalid file type for certificate. Supported types are JPEG, PNG, PDF, DOC."}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if aadhaar_card and aadhaar_card.content_type not in allowed_image_types:
            return Response({"message": "Invalid file type for Aadhaar card. Supported types are JPEG, PNG, PDF, DOC."}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if poa and poa.content_type not in allowed_image_types:
            return Response({"message": "Invalid file type for POA. Supported types are JPEG, PNG, PDF, DOC."}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if poi and poi.content_type not in allowed_image_types:
            return Response({"message": "Invalid file type for POI. Supported types are JPEG, PNG, PDF, DOC."}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if tc and tc.content_type not in allowed_image_types:
            return Response({"message": "Invalid file type for TC. Supported types are JPEG, PNG, PDF, DOC."}, status=status.HTTP_406_NOT_ACCEPTABLE)

        class_name=request.data['class_name']
        section= request.data['section']
        session= request.data['session']
        date_of_joining=request.data['date_of_joining']
        date_of_joining = datetime.strptime(request.data.get('date_of_joining' ), '%Y-%m-%d').date()

        student = Student.objects.create(
            name=name,
            gender=gender,
            adhar_card_number=adhar_card_number,
            dob=dob,
            identification_marks=identification_marks,
            category=category,
            height=height,
            weight=weight,
            mail_id=mail_id,
            contact_detail=contact_detail,
            address=address
        )
        parent=Parent.objects.create(student=student,father_name=father_name,father_qualification=father_qualification,father_profession=father_profession,father_designation=father_designation,father_aadhar_card=father_aadhar_card,
                                     father_mobile_number=father_mobile_number,father_mail_id=father_mail_id,mother_name=mother_name,mother_qualification=mother_qualification,mother_profession=mother_profession,
                                     mother_designation=mother_designation,mother_aadhar_card=mother_aadhar_card,mother_mobile_number=mother_mobile_number,mother_mail_id=mother_mail_id)
      
        academic_details, created = AcademicDetails.objects.update_or_create(
                student=student,
                defaults={
                    'class_name': class_name,
                    'section': section,
                    'date_of_joining': date_of_joining,
                    'session':session
                }
            )
        document = Document.objects.create(
            student=student,
            certificate=certificate,
            aadhaar_card=aadhaar_card,
            poa=poa,
            poi=poi,
            tc=tc
        )
        send_student_mail(student, academic_details)
        send_admin_notification(student, academic_details)
        response_data = {
            'message': 'Student data created successfully',
            'student_id': student.id,
            'document_id': document.id,
            'parent':parent.id,
            'academic details':academic_details.id
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
