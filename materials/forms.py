from datetime import datetime

from django.forms.formsets import formset_factory
from django import forms
from django.core.exceptions import ValidationError
from django.forms import CharField, ModelForm, inlineformset_factory
from .models import *
import time
from crispy_forms.helper import FormHelper
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton

from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab

class VehiculeForm(ModelForm):
    KILOMETRE = (
        ('1', 'Kilometres'),
        ('2', 'Miles'),
    )
    metrage = forms.ChoiceField(choices=KILOMETRE)
    class Meta:
        model = Vehicule
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
            'immatriculation': forms.TextInput(attrs={'placeholder': 'par Ex: 1797 WS CI 01'}),
        }