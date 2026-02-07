from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import Message, AudioMessage


class MessageModelTest(TestCase):
    """Test Message model"""
    
    def setUp(self):
        self.message = Message.objects.create(
            role='patient',
            original_text='I have a headache',
            translated_text='The patient reports headache symptoms'
        )
    
    def test_message_creation(self):
        """Test that a message can be created"""
        self.assertEqual(self.message.role, 'patient')
        self.assertTrue(self.message.id)
    
    def test_message_string_representation(self):
        """Test message string representation"""
        self.assertIn('PATIENT', str(self.message))


class AudioMessageModelTest(TestCase):
    """Test AudioMessage model"""
    
    def setUp(self):
        self.audio_msg = AudioMessage.objects.create(
            role='doctor',
            transcription_status='pending'
        )
    
    def test_audio_message_creation(self):
        """Test that an audio message can be created"""
        self.assertEqual(self.audio_msg.role, 'doctor')
        self.assertEqual(self.audio_msg.transcription_status, 'pending')


class APIEndpointTest(TestCase):
    """Test API endpoints"""
    
    def test_get_messages_endpoint(self):
        """Test GET /api/messages/"""
        Message.objects.create(
            role='patient',
            original_text='Test message',
            translated_text='Translated test'
        )
        response = self.client.get('/api/messages/')
        self.assertEqual(response.status_code, 200)
