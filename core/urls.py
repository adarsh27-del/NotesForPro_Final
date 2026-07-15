from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from core.views import web_login, dashboard, web_logout,register_page   # adjust import path
from django.views.generic import RedirectView

urlpatterns = [
    re_path(r'^accounts/login/$', RedirectView.as_view(url='/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include(('api.urls', 'api'), namespace='api')),

    # Web routes
    path('login/', web_login, name='login'),
    path('', dashboard, name='dashboard'),
    path('logout/', web_logout, name='logout'),
    path('register/', register_page, name='register_page'),
    path('notes/', include('notes.urls')),
    path('tasks/', include('tasks.urls')),
    path('ai-tools/', include('ai_tools.urls')),
    path('mindmap/', include('mindmap.urls')),
    path('graphs/', include('graph.urls')),
    path('whiteboard/', include('whiteboard.urls')),
    path('games/', include('games.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)