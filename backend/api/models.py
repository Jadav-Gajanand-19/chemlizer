from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UploadHistory(models.Model):
    """Model to track CSV upload history (keep only last 5)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    uploaded_at = models.DateTimeField(default=timezone.now)
    filename = models.CharField(max_length=255)
    num_records = models.IntegerField(default=0)
    
    # Summary statistics
    avg_flowrate = models.FloatField(null=True, blank=True)
    avg_pressure = models.FloatField(null=True, blank=True)
    avg_temperature = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = 'Upload Histories'
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class Equipment(models.Model):
    """Model to store chemical equipment data"""
    upload_session = models.ForeignKey(UploadHistory, on_delete=models.CASCADE, related_name='equipment')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    class Meta:
        ordering = ['equipment_name']
        verbose_name_plural = 'Equipment'
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"
