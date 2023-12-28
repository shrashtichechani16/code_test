from rest_framework import serializers

class CSVFileUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()
