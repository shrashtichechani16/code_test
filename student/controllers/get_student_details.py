from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from student.models import Student,Parent,AcademicDetails,Document

@api_view(['GET'])
def get_student_details(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        parent = Parent.objects.filter(student=student).first()
        academic_details = AcademicDetails.objects.filter(student=student).first()
        document=Document.objects.filter(student=student).first()
        student_data = {
            'id': student.id,
            'name': student.name,
            'gender': student.gender,
            'adhar_card_number': student.adhar_card_number,
            'dob': student.dob,
            'identification_marks': student.identification_marks,
            'category': student.category,
            'height': student.height,
            'weight': student.weight,
            'mail_id': student.mail_id,
            'contact_detail': student.contact_detail,
            'address': student.address,
            'created_at': student.created_at,
            'updated_at': student.updated_at,
            'parent': {
                'father_name': parent.father_name ,
                'father_qualification': parent.father_qualification ,
                'father_profession': parent.father_profession ,
                'father_designation': parent.father_designation ,
                'father_aadhar_card': parent.father_aadhar_card ,
                'father_mobile_number': parent.father_mobile_number ,
                'father_mail_id': parent.father_mail_id ,
                'mother_name': parent.mother_name ,
                'mother_qualification': parent.mother_qualification ,
                'mother_profession': parent.mother_profession ,
                'mother_designation': parent.mother_designation ,
                'mother_aadhar_card': parent.mother_aadhar_card ,
                'mother_mobile_number': parent.mother_mobile_number ,
                'mother_mail_id': parent.mother_mail_id ,
            },
            'academic_details': {
                'enrollment_id':academic_details.enrollment_id ,
                'class_name': academic_details.class_name ,
                'section': academic_details.section ,
                'date_of_joining': academic_details.date_of_joining ,
                'session':academic_details.session
            },
            'document': {
                'certificate': str(document.certificate) ,
                'aadhaar_card': str(document.aadhaar_card) ,
                'poa': str(document.poa),
                'poi': str(document.poi),
                'tc': str(document.tc),
                'created_at': document.created_at,
                'updated_at': document.updated_at,
            }
        }

        return Response(student_data, status=status.HTTP_200_OK)

    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
