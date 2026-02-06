from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from openai import OpenAI
import os

@api_view(['POST'])
def translate_medical_text(request):
    client = OpenAI(api_key="YOUR_OPENAI_API_KEY_HERE")
    
    text_to_translate = request.data.get('text')
    target_language = request.data.get('language', 'Spanish')

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are a medical translator. Translate the following doctor's statement into {target_language} so a patient can understand it clearly."},
            {"role": "user", "content": text_to_translate}
        ]
    )
    
    return Response({"translation": response.choices[0].message.content})