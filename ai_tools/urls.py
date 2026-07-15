from django.urls import path
from . import views

urlpatterns = [

    path("", views.dashboard, name="dashboard"),

    path("summarize/", views.summarize),
    path("translate/", views.translate),
    path("generate/", views.generate_content),
    path("ocr/", views.ocr),
    path("meeting-notes/", views.meeting_notes),
    path("generate-image/", views.generate_image),

]