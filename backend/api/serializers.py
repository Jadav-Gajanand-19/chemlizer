from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Equipment, UploadHistory


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for Equipment model"""
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class UploadHistorySerializer(serializers.ModelSerializer):
    """Serializer for UploadHistory model"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UploadHistory
        fields = ['id', 'filename', 'username', 'uploaded_at', 'num_records',
                  'avg_flowrate', 'avg_pressure', 'avg_temperature']


class CSVUploadSerializer(serializers.Serializer):
    """Serializer for CSV file upload"""
    file = serializers.FileField()
    
    def validate_file(self, value):
        """Validate that uploaded file is CSV"""
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        return value
