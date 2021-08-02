import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


# Create your models here.
class Materiels(models.Model):
    name = models.CharField(verbose_name=("Nom du matériel"), max_length=50, unique=True, null=True, blank=True)
    reference = models.CharField(verbose_name=("Reference"), max_length=50, unique=True)
    fabricat_year = models.PositiveIntegerField(verbose_name=("Année du Model"),
                                                default=current_year(),
                                                validators=[MinValueValidator(1984), max_value_current_year])
    description = models.TextField(verbose_name=("Observation"), null=True, blank=True)
    valeur_cat = models.IntegerField(verbose_name=("Valeur Catalogue"), null=True, blank=True)
    valeur_achat = models.IntegerField(verbose_name=("Valeur Achat"), null=True, blank=True)
    valeur_residuel = models.IntegerField(verbose_name=("Valeur Residuel"), null=True, blank=True)

    class Meta:
        abstract = True


class Localite(models.Model):
    libelle = models.CharField(verbose_name=("Nom du matériel"), max_length=50)


class Batiments(Materiels):
    nbre_piece = models.CharField(verbose_name=("Nom du matériel"), max_length=50)
    nbre_etage = models.CharField(verbose_name=("Reference"), max_length=50)
    latitude = models.FloatField(verbose_name=("Latitude"), max_length=50)
    longitude = models.FloatField(verbose_name=("Latitude"), max_length=50)
    # materiel_id = models.ForeignKey(Materiels, verbose_name=("Materiel"), on_delete=models.CASCADE)
    localite_id = models.ForeignKey(Localite, verbose_name=("Localite"), on_delete=models.CASCADE)


class Fabricant(models.Model):
    libelle = models.CharField(verbose_name=("Libelle Marque"), max_length=50)
    abreviate = models.CharField(verbose_name=("Abreviation Marque"), max_length=50)
    image = models.ImageField(verbose_name=("Logo Marque"), upload_to="static/media/marque/", height_field=None,
                              width_field=None,
                              max_length=300)

    def __str__(self):
        return self.libelle


class Model(models.Model):
    libelle = models.CharField(verbose_name=("Libelle Type Energie"), max_length=50)
    fabricant_id = models.ForeignKey(Fabricant, verbose_name=("Fabricant"), on_delete=models.CASCADE)

    def __str__(self):
        return self.fabricant_id.libelle + '/' + self.libelle


class Electronique(Materiels):
    numero_serie = models.CharField(verbose_name=("Nom du matériel"), max_length=50)
    model_id = models.ForeignKey(Model, verbose_name=("Model"), on_delete=models.CASCADE)
    # fabricant_id = models.ForeignKey(Fabricant, verbose_name=("Fabricant"), on_delete=models.CASCADE)


class TypeEnergieVehicule(models.Model):
    libelle = models.CharField(verbose_name=("Libelle Type Energie"), max_length=50)

    def __str__(self):
        return self.libelle


class Typevehicule(models.Model):
    libelle = models.CharField(verbose_name=("Libelle Type Energie"), max_length=50)
    nbre_roue = models.IntegerField(verbose_name=("Nombre de Roue Vehicule"))

    def __str__(self):
        return self.libelle


class Vehicule(Materiels):
    TYPE_TRANSMISSION = (
        ('1', 'Manuel'),
        ('2', 'Automatique'),
    )
    immatriculation = models.CharField(verbose_name=("Immatriculation Vehicule"), max_length=50, unique=True)
    last_kilometrage = models.IntegerField(verbose_name=("Dernier kilometrage Vehicule (Km/Milles)"), null=True, blank=True, default=0)
    num_chassi = models.CharField(verbose_name=("Numero de Chassi Vehicule"), max_length=50,  unique=True)
    couleur = models.CharField(verbose_name=("Couleur du Vehicule"), max_length=50)
    # nbre_roue = models.IntegerField(verbose_name=("Nombre de Roue Vehicule"), max_length=50)
    nbre_porte = models.IntegerField(verbose_name=("Nombre de Porte Vehicule"), default=5)
    type_transmissin = models.CharField(max_length=1, choices=TYPE_TRANSMISSION)
    nbre_chevaux = models.IntegerField(verbose_name=("Nombre de cheveaux"))
    puissance_fiscal = models.IntegerField(verbose_name=("Puissance"))

    type_energie_id = models.ForeignKey(TypeEnergieVehicule, verbose_name=("Type d'Energie"), on_delete=models.CASCADE)
    Typevehicule = models.ForeignKey(Typevehicule, verbose_name=("Type de Véhicule"), on_delete=models.CASCADE)
    model_id = models.ForeignKey(Model, verbose_name=("Model"), on_delete=models.CASCADE)


    @property
    def set_name(self, value):
      self.name = self.immatriculation
    @property
    def get_name(self, value):
        return  self.name

    def save(self, *args, **kwargs):
        self.name = self.immatriculation
        super(Vehicule, self).save(*args, **kwargs)

class TypeVetement(models.Model):
    name = models.CharField(verbose_name=("Libelle type de vetement"), max_length=50)

    class Meta:
        verbose_name = ("Type de Vetement")
        verbose_name_plural = ("Type de Vetements")

    def __str__(self):
        return self.name


class TailleVetement(models.Model):
    name = models.CharField(verbose_name=("Taille de vetement"), max_length=50)
    taille_fr = models.CharField(verbose_name=("Taille FR de vetement"), max_length=50)

    class Meta:
        verbose_name = ("Taille de Vetement")
        verbose_name_plural = ("Taille de Vetements")

    def __str__(self):
        return self.name


class Vetement(Materiels):
    taille = models.CharField(verbose_name=("Taille Vetement"), max_length=50)
    couleur = models.CharField(verbose_name=("Couleur Vetement"), max_length=50)
    materiel_utilisé = models.CharField(verbose_name=("Materiel Utilisé"), max_length=50)
    type_vetement_id = models.ForeignKey(TypeVetement, verbose_name=("type vetement"), on_delete=models.CASCADE)
    taille_id = models.ForeignKey(TailleVetement, verbose_name=("taille vetement"), on_delete=models.CASCADE)
