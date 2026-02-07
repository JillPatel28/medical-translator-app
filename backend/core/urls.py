from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse 

def home_view(request):
    return HttpResponse(
        "<h1>Backend Running</h1>"
        "<p>The API is available at <a href='/api/'>/api/</a></p>"
        "<p><strong>Tip:</strong> To see your React App, go to <a href='http://localhost:5173'>http://localhost:5173</a></p>"
    )

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)