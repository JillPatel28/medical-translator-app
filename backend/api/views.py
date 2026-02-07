from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Message, AudioMessage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from openai import OpenAI
from datetime import datetime
import os

@csrf_exempt
def api_root(request):
    """API root endpoint - shows available endpoints"""
    return JsonResponse({
        'status': 'success',
        'message': 'Doctor-Patient Translation API',
        'version': '1.0',
        'endpoints': {
            'translate': '/api/translate/',
            'audio': '/api/audio/',
            'summarize': '/api/summarize/',
            'messages': '/api/messages/',
            'audio-messages': '/api/audio-messages/',
            'search': '/api/search/'
        }
    })

def get_openai_client():
    """Initialize OpenAI client"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return OpenAI(api_key=api_key)

@csrf_exempt
@require_http_methods(["POST"])
def translate_text(request):
    """Translate medical text between doctor and patient language"""
    try:
        data = json.loads(request.body)
        role = data.get('role', 'doctor')
        text = data.get('text', '')
        
        if not text:
            return JsonResponse({'error': 'Text is required'}, status=400)
        
        # Save message
        message = Message.objects.create(role=role, text=text)
        
        # Get AI translation/explanation
        client = get_openai_client()
        
        if role == 'doctor':
            prompt = f"Translate this medical terminology to patient-friendly language: {text}"
        else:
            prompt = f"Help the doctor understand this patient statement in medical terms: {text}"
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical translation assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        
        translated = response.choices[0].message.content
        
        return JsonResponse({
            'status': 'success',
            'message': {
                'id': message.id,
                'role': message.role,
                'text': message.text,
                'timestamp': message.timestamp.isoformat(),
                'translation': translated
            }
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def translate_audio(request):
    """Process audio file and convert to text"""
    try:
        audio_file = request.FILES.get('audio')
        role = request.POST.get('role', 'doctor')
        
        if not audio_file:
            return JsonResponse({'error': 'Audio file is required'}, status=400)
        
        # Save audio message
        audio_message = AudioMessage.objects.create(role=role, audio_file=audio_file)
        
        # Use OpenAI to transcribe
        client = get_openai_client()
        
        # Read audio file
        audio_content = audio_file.read()
        
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.webm", audio_content, "audio/webm")
        )
        
        audio_message.transcript = transcript.text
        audio_message.save()
        
        # Also save as regular message
        message = Message.objects.create(role=role, text=transcript.text)
        
        return JsonResponse({
            'status': 'success',
            'message': {
                'id': message.id,
                'role': message.role,
                'text': message.text,
                'timestamp': message.timestamp.isoformat()
            }
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_messages(request):
    """Get all messages"""
    try:
        messages = Message.objects.all().values('id', 'role', 'text', 'timestamp')
        return JsonResponse({
            'status': 'success',
            'messages': list(messages)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_audio_messages(request):
    """Get all audio messages"""
    try:
        audio_messages = AudioMessage.objects.all().values('id', 'role', 'transcript', 'timestamp')
        return JsonResponse({
            'status': 'success',
            'audio_messages': list(audio_messages)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def search_messages(request):
    """Search messages by keyword"""
    try:
        data = json.loads(request.body)
        keyword = data.get('keyword', '')
        
        messages = Message.objects.filter(text__icontains=keyword).values('id', 'role', 'text', 'timestamp')
        
        return JsonResponse({
            'status': 'success',
            'messages': list(messages)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def summarize_conversation(request):
    """Summarize selected messages"""
    try:
        data = json.loads(request.body)
        message_ids = data.get('message_ids', [])
        
        if not message_ids:
            return JsonResponse({'error': 'No messages selected'}, status=400)
        
        messages = Message.objects.filter(id__in=message_ids)
        conversation_text = "\n".join([f"{msg.role}: {msg.text}" for msg in messages])
        
        client = get_openai_client()
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical conversation summarizer."},
                {"role": "user", "content": f"Summarize this doctor-patient conversation:\n{conversation_text}"}
            ],
            max_tokens=300
        )
        
        summary = response.choices[0].message.content
        
        return JsonResponse({
            'status': 'success',
            'summary': summary
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)