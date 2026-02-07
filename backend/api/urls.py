from django.urls import path
from .views import (
    api_root,
    translate_text,
    translate_audio,
    summarize_conversation,
    get_messages,
    get_audio_messages,
    search_messages
)

urlpatterns = [
    path("", api_root, name="api_root"),
    path("translate/", translate_text, name="translate_text"),
    path("audio/", translate_audio, name="translate_audio"),
    path("summarize/", summarize_conversation, name="summarize"),
    path("messages/", get_messages, name="get_messages"),
    path("audio-messages/", get_audio_messages, name="get_audio_messages"),
    path("search/", search_messages, name="search_messages"),
]