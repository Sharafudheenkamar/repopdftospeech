from django.forms import ModelForm
from .models import *



class UserRegform(ModelForm):
    class Meta:
        model= LoginTable
        fields = '__all__'

