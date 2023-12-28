from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from datetime import datetime
from student.models import Student, Parent, AcademicDetails, Document

@api_view(['PUT'])
@transaction.atomic
def update_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)

        student.name = request.data.get('name', student.name)
        student.gender = request.data.get('gender', student.gender)
        student.adhar_card_number = request.data.get('adhar_card_number', student.adhar_card_number)
        student.dob = request.data.get('dob', student.dob)
        student.identification_marks = request.data.get('identification_marks', student.identification_marks)
        student.category = request.data.get('category', student.category)
        student.height = request.data.get('height', student.height)
        student.weight = request.data.get('weight', student.weight)
        student.mail_id = request.data.get('mail_id', student.mail_id)
        student.contact_detail = request.data.get('contact_detail', student.contact_detail)
        student.address = request.data.get('address', student.address)
        student.save()
        parent = student.parents.first()
        parent.father_name = request.data.get('father_name', parent.father_name)
        parent.father_qualification = request.data.get('father_qualification', parent.father_qualification)
        parent.father_profession = request.data.get('father_profession', parent.father_profession)
        parent.father_designation = request.data.get('father_designation', parent.father_designation)
        parent.father_aadhar_card = request.data.get('father_aadhar_card', parent.father_aadhar_card)
        parent.father_mobile_number = request.data.get('father_mobile_number', parent.father_mobile_number)
        parent.father_mail_id = request.data.get('father_mail_id', parent.father_mail_id)
        parent.mother_name = request.data.get('mother_name', parent.mother_name)
        parent.mother_qualification = request.data.get('mother_qualification', parent.mother_qualification)
        parent.mother_profession = request.data.get('mother_profession', parent.mother_profession)
        parent.mother_designation = request.data.get('mother_designation', parent.mother_designation)
        parent.mother_aadhar_card = request.data.get('mother_aadhar_card', parent.mother_aadhar_card)
        parent.mother_mobile_number = request.data.get('mother_mobile_number', parent.mother_mobile_number)
        parent.mother_mail_id = request.data.get('mother_mail_id', parent.mother_mail_id)
        parent.save()
        academic_details = student.academic_details.first()
        academic_details.class_name = request.data.get('class_name', academic_details.class_name)
        academic_details.section = request.data.get('section', academic_details.section)
        academic_details.session=request.data.get('session',academic_details.session)
        academic_details.date_of_joining = datetime.strptime(request.data.get('date_of_joining'), '%Y-%m-%d').date() if request.data.get('date_of_joining') else academic_details.date_of_joining   
        document = student.document.first()
        document.certificate = request.FILES.get('certificate', document.certificate)
        document.aadhaar_card = request.FILES.get('aadhaar_card', document.aadhaar_card)
        document.poa = request.FILES.get('poa', document.poa)
        document.poi = request.FILES.get('poi', document.poi)
        document.tc = request.FILES.get('tc', document.tc)
        document.save()


        response_data = {
            'message': 'Student data updated successfully',
            'student_id': student.id,
            'document_id': document.id,
            'parent_id': parent.id,
            'academic_details_id': academic_details.id
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
