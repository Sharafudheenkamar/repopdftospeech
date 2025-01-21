# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('',MainPage.as_view(),name='MainPage'),
    path('UserReg',UserReg.as_view(),name='UserReg'),
    path('homepage',homepage.as_view(),name='homepage'),


    # path('upload', pdf_to_speech, name='pdf_to_speech'),
]
