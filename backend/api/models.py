from django.db import models

class Message(models.Model):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    text = models.TextField(blank=True, null=True)  # FIXED: Added blank=True, null=True
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.role}: {self.text[:50] if self.text else 'No text'}"


class AudioMessage(models.Model):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    audio_file = models.FileField(upload_to='audio_messages/', null=True, blank=True)
    transcript = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.role} Audio: {self.timestamp}"