# views.py
import os
from PyPDF2 import PdfReader
from django.views import View
from gtts import gTTS
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from deep_translator import GoogleTranslator
from .models import *


# Create your views here.
class MainPage(View):
    def get(self, request):
        return render(request, "mainpage.html")
class LoginPage(View): 
    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        UserName = request.POST['UserName']
        PassWord = request.POST['PassWord']
        try:
            login_obj = LoginTable.objects.get(UserName=UserName, PassWord=PassWord)
            if login_obj.type == "admin":
                return HttpResponse('''<script>window.location="/AdminDashboardPage/"</script>''')
            elif login_obj.type == "manufacture":
                return HttpResponse('''<script>window.location="/ManufactureDashboardPage/"</script>''')
            else:
                return HttpResponse('''<script>alert('contact admin for approval');window.location="/"</script>''')
        except LoginTable.DoesNotExist:
            return HttpResponse('''<script>alert('invalid username and password');window.location="/"</script>''')
     
class UserReg(View):
     def get(self, request):
        return render(request, "Register.html")
     def post(self, request):
         form = manufactureform(request.POST)
         if form.is_valid():
            c=form.save(commit=False)
            d=LoginTable.objects.create(UserName=request.POST['username'],PassWord=request.POST['password'],type='pending')
            print(d)
            c.LOGINID=d
            c.save()
            return HttpResponse('''<script>alert("registered");window.location=("/")</script>''')

    
def pdf_to_speech(request):
    if request.method == 'POST' and request.FILES['pdf']:
        pdf_file = request.FILES['pdf']
        target_language = request.POST.get('language', 'en')

        # Save the uploaded file
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        pdf_path = fs.path(filename)

        # Extract text from the PDF
        reader = PdfReader(pdf_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        print(text)
        # Translate text
        translator = GoogleTranslator(source='auto', target=target_language)
        translated_text = translator.translate(text)
        # Convert translated text to speech
        tts = gTTS(translated_text, lang=target_language)
        audio_path = os.path.join(fs.location, 'media/output.mp3')
        tts.save(audio_path)

        # Serve the audio file
        with open(audio_path, 'rb') as audio_file:
            response = HttpResponse(audio_file, content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="output.mp3"'
            return response

    return render(request, 'pdf_to_speech.html')
