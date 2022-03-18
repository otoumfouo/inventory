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
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        
class MaterielsForm(ModelForm):
    class Meta:
        model = Materiels
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
        }

class EntrepotsForm(ModelForm):
    class Meta:
        model = Entrepots
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
            'Adresse': forms.Textarea(attrs={'cols': 50, 'rows': 2}),
        }


class SitesForm(ModelForm):
    class Meta:
        model = Site
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
            'Adresse': forms.Textarea(attrs={'cols': 50, 'rows': 2}),
        }


class BonLivraisonForm(ModelForm):
    site = forms.ModelChoiceField(queryset=Site.objects.all(),  empty_label="")
    class Meta:
        model = Entrepots
        fields = '__all__'


class DetailsForm(ModelForm):

    class Meta:
        model = BonLivraisonDetail
        exclude = ('bonCommande',)
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['materiel'].widget.attrs.update({
            'class': 'info form-control form-control-rounded'
        })
        self.fields['materiel'].label = "Matériels"
        self.fields['qte'].label = "Quantité"
        self.fields['qte'].widget.attrs.update({
            'class': 'form-control form-control-rounded'
        })
        self.fields['etatMateriel'].label = "Etat"
        self.fields['etatMateriel'].widget.attrs.update({
            'class': 'form-control form-control-rounded'
        })


RequistionRequestFormSet = inlineformset_factory(BonLivraison, BonLivraisonDetail,
                                                 form=DetailsForm, can_delete=True, extra=5)


class MaterielsVehiculeForm(ModelForm):
    class Meta:
        model = Materiels
        fields = '__all__'
        exclude = ('name','en_stock', 'type')
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
        }

class VehiculeForm(ModelForm):
    KILOMETRE = (
        ('1', 'Kilometres'),
        ('2', 'Miles'),
    )
    #metrage = forms.ChoiceField(choices=KILOMETRE, )

    class Meta:
        model = Vehicule
        fields = '__all__'
        exclude = ('materials',)
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
            'immatriculation': forms.TextInput(attrs={'placeholder': 'par Ex: 1797 WS CI 01'}),
        }


class SearchForm(forms.Form):
    site = forms.ModelChoiceField(queryset=Site.objects.all(), required=True)
    bureau = forms.ModelChoiceField(queryset=Entrepots.objects.all(), required=False)

class SearchCatForm(forms.Form):
    TYPE_MATERIEL = (

        ('Materiel Informatique', 'Materiel Informatique'),
        ('Equipement Scientifique & Technique', 'Equipement Scientifique & Technique'),
        ('Mobilier & Equipement de Bureau', 'Mobilier & Equipement de Bureau'),
        ('Matériel de Sécurité', 'Matériel de Sécurité'),
        ('Matériel de Transmission', 'Matériel de Transmission'),
        ('Autres', 'Autres'),
    )

    materiel = forms.ModelChoiceField(queryset=Materiels.objects.all(), required=False)
    categorie_materiel = forms.ChoiceField(choices=TYPE_MATERIEL,required=True )

