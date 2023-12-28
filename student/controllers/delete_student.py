from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from student.models import Student,Parent,AcademicDetails,Document

@api_view(['DELETE'])
def delete_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)

        parent = Parent.objects.filter(student=student).first()
        academic_details = AcademicDetails.objects.filter(student=student).first()
        document = Document.objects.filter(student=student).first()

        if parent:
            parent.delete()
        if academic_details:
            academic_details.delete()
        if document:
            document.delete()

        student.delete()

        return Response({'message': 'Student and related data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
