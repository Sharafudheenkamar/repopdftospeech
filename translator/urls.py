# urls.py
from django.urls import path
from translator.views import pdf_to_speech

urlpatterns = [
    path('', pdf_to_speech, name='pdf_to_speech'),
]
