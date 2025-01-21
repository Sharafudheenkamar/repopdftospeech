# views.py
import os
from django.core.files.base import File
from PyPDF2 import PdfReader
from django.views import View
from gtts import gTTS
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from deep_translator import GoogleTranslator

from .form import UserRegform
from .models import *


# Create your views here.
class MainPage(View):
    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        UserName = request.POST['UserName']
        PassWord = request.POST['PassWord']
        try:
            login_obj = LoginTable.objects.get(UserName=UserName, PassWord=PassWord)
            if login_obj.type == "user":
                return HttpResponse('''<script>window.location="/homepage"</script>''')
        except LoginTable.DoesNotExist:
            return HttpResponse('''<script>alert('invalid username and password');window.location="/"</script>''')
     


class UserReg(View):
     def get(self, request):
        return render(request, "register.html")
     def post(self, request):
         form = UserRegform(request.POST)
         if form.is_valid():
            c=form.save(commit=False)
            
            # d=LoginTable.objects.create(UserName=request.POST['UserName'],PassWord=request.POST['PassWord'],type='user')
            # print(d)
            # c.LOGINID=d
            c.save()
            return HttpResponse('''<script>alert("registered");window.location=("/")</script>''')

class homepage(View):
    def get(self, request):
        return render(request, "home.html")
    def post(self,request):
        pdf_file = request.FILES['pdf']
        target_language = request.POST.get('language', 'en')

        # Save the uploaded PDF to the database
        pdf_instance = PDFFile(file=pdf_file)
        pdf_instance.save()

        # Extract text from the PDF
        pdf_path = pdf_instance.file.path  # Get the saved file's path
        reader = PdfReader(pdf_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()

        # Translate text
        translator = GoogleTranslator(source='auto', target=target_language)
        translated_text = translator.translate(text)

        # Convert translated text to speech
        tts = gTTS(translated_text, lang=target_language)
        audio_filename = f"{os.path.splitext(pdf_file.name)[0]}_output.mp3"
        audio_path = os.path.join('media/audios/', audio_filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        tts.save(audio_path)

        # Save the audio file to the model
        with open(audio_path, 'rb') as audio_file:
            pdf_instance.audio.save(audio_filename, File(audio_file))

        pdf_instance.save()

        # Serve the audio file as a response
        response = HttpResponse(pdf_instance.audio, content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename="{audio_filename}"'
    
        # Pass the audio file URL to the template
        audio_url = pdf_instance.audio.url
        print(audio_url)
        return render(request, 'home.html', {'audio_url': audio_url})