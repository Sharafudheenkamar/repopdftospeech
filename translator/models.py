# models.py
from django.db import models


# Create your models here.
class LoginTable(models.Model):
    UserName = models.CharField(max_length=100, null=True, blank=True)
    PassWord = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
class PDFFile(models.Model):
    file = models.FileField(upload_to='pdfs/',null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    audio =models.FileField(upload_to='audios/',null=True, blank=True)
