import csv
from io import TextIOWrapper
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from student.controllers.tasks import process_csv_data
from ..serializers import CSVFileUploadSerializer

@api_view(['POST'])
def csv_file_upload(request):
    serializer = CSVFileUploadSerializer(data=request.data)
    if serializer.is_valid():
        csv_file = request.FILES['csv_file']
        csv_data = TextIOWrapper(csv_file.file, encoding=request.encoding)
        process_csv_data.delay(csv_data.read())
        return Response({'message': 'CSV file is being processed.'}, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
