from django.contrib import admin
from .models import Message, AudioMessage


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Message model"""
    
    list_display = [
        'id',
        'role',
        'text_preview',
        'timestamp'
    ]
    list_filter = [
        'role',
        'timestamp'
    ]
    search_fields = [
        'text',
    ]
    readonly_fields = [
        'id',
        'timestamp'
    ]
    fieldsets = (
        ('Message Info', {
            'fields': ('id', 'role', 'timestamp')
        }),
        ('Content', {
            'fields': ('text',)
        }),
    )
    
    def text_preview(self, obj):
        """Show preview of text"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'
    
    ordering = ['-timestamp']


@admin.register(AudioMessage)
class AudioMessageAdmin(admin.ModelAdmin):
    """Admin interface for AudioMessage model"""
    
    list_display = [
        'id',
        'role',
        'audio_file_name',
        'transcript_preview',
        'timestamp'
    ]
    list_filter = [
        'role',
        'timestamp'
    ]
    search_fields = [
        'transcript',
        'role'
    ]
    readonly_fields = [
        'id',
        'timestamp',
        'audio_preview'
    ]
    fieldsets = (
        ('Audio Info', {
            'fields': ('id', 'role', 'timestamp')
        }),
        ('File Details', {
            'fields': ('audio_file', 'audio_preview')
        }),
        ('Transcript', {
            'fields': ('transcript',)
        })
    )
    
    def audio_file_name(self, obj):
        """Show audio file name"""
        if obj.audio_file:
            return obj.audio_file.name.split('/')[-1]
        return 'No file'
    audio_file_name.short_description = 'Audio File'
    
    def transcript_preview(self, obj):
        """Show preview of transcript"""
        if obj.transcript:
            return obj.transcript[:50] + '...' if len(obj.transcript) > 50 else obj.transcript
        return 'No transcript'
    transcript_preview.short_description = 'Transcript'
    
    def audio_preview(self, obj):
        """Show audio player in admin"""
        if obj.audio_file:
            from django.utils.html import format_html
            return format_html(
                '<audio controls style="width: 100%; margin-top: 10px;">'
                '<source src="{}" type="audio/webm">'
                'Your browser does not support the audio element.'
                '</audio>',
                obj.audio_file.url
            )
        return 'No audio file'
    audio_preview.short_description = 'Audio Preview'
    
    ordering = ['-timestamp']