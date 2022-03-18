import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


'''
ce model trace si le matériel est attribution ou non

class StatutMateriel(models.Model):
    libelle = models.CharField(verbose_name=("Statut du Martéiel"), max_length=50)
'''


class EtatMateriel(models.Model):
    libelle = models.CharField(verbose_name=("Statut du Martéiel"), max_length=50)
    def __str__(self):
        return str(self.libelle)


class ModeAcquisition(models.Model):
    libelle = models.CharField(verbose_name=("Mode acquistion"), max_length=50)
    def __str__(self):
        return str(self.libelle)


class CategorieMateriel(models.Model):
    libelle = models.CharField(verbose_name=("Mode acquistion"), max_length=50)
    def __str__(self):
        return str(self.libelle)

class Fabricant(models.Model):
    libelle = models.CharField(verbose_name=("Libelle Marque"), max_length=50)
    abreviate = models.CharField(verbose_name=("Abreviation Marque"), max_length=50)
    image = models.ImageField(verbose_name=("Logo Marque"), upload_to="static/media/marque/", height_field=None,
                              width_field=None,
                              max_length=300, null=True, blank=True)

    def __str__(self):
        return self.libelle

# Create your models here.
class Materiels(models.Model):
    TYPE_MATERIEL = (

        ('Materiel Informatique', 'Materiel Informatique'),
        ('Equipement Scientifique & Technique', 'Equipement Scientifique & Technique'),
        ('Mobilier & Equipement de Bureau', 'Mobilier & Equipement de Bureau'),
        ('Matériel de Sécurité', 'Matériel de Sécurité'),
        ('Matériel de Transmission', 'Matériel de Transmission'),
        ('Autres', 'Autres'),
    )
    name = models.CharField(verbose_name=("Nom du matériel"), max_length=50, unique=True, null=True, blank=True)
    reference = models.CharField(verbose_name=("Reference "), max_length=50, unique=True)
    fabricat_year = models.PositiveIntegerField(verbose_name=("Année Acquisition"), null=True, blank=True,
                                                default=current_year(),
                                                validators=[MinValueValidator(1984), max_value_current_year])
    description = models.TextField(verbose_name=("Observation"), null=True, blank=True)
    valeur_cat = models.IntegerField(verbose_name=("Valeur Catalogue"), null=True, blank=True)
    valeur_achat = models.IntegerField(verbose_name=("Valeur Achat"), null=True, blank=True)
    valeur_residuel = models.IntegerField(verbose_name=("Valeur Residuel"), null=True, blank=True)
    en_stock = models.BooleanField(default=True,null=True, blank=True)
    #type = models.CharField(max_length=50, choices=TYPE_MATERIEL, default="Autres")
    type = models.ForeignKey(CategorieMateriel, verbose_name=("Catégorie Matériel"), on_delete=models.CASCADE)
    mode_acquisition = models.ForeignKey(ModeAcquisition, verbose_name=("Mode Acquisition"), on_delete=models.CASCADE)
    frabriquant = models.ForeignKey(Fabricant, verbose_name=("Marque"), null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        #return str(self.name)+"  "+str(self.frabriquant.libelle)
        return str(self.name)


class Localite(models.Model):
    libelle = models.CharField(verbose_name=("localite"), max_length=50)


class Pays(models.Model):
    name = models.CharField(verbose_name=("Nom"), max_length=50)
    abrev = models.CharField(verbose_name=("localite"), max_length=50)


class Batiments(models.Model):
    materials = models.ForeignKey(Materiels, verbose_name=("materiel"), on_delete=models.CASCADE)
    nbre_piece = models.CharField(verbose_name=("Nom du matériel"), max_length=50)
    nbre_etage = models.CharField(verbose_name=("Reference"), max_length=50)
    latitude = models.FloatField(verbose_name=("Latitude"), max_length=50)
    longitude = models.FloatField(verbose_name=("Latitude"), max_length=50)
    # materiel_id = models.ForeignKey(Materiels, verbose_name=("Materiel"), on_delete=models.CASCADE)
    localite_id = models.ForeignKey(Localite, verbose_name=("Localite"), on_delete=models.CASCADE)




class Model(models.Model):
    libelle = models.CharField(verbose_name=("Libelle Type Energie"), max_length=50)
    fabricant_id = models.ForeignKey(Fabricant, verbose_name=("Fabricant"), on_delete=models.CASCADE)

    def __str__(self):
        return self.fabricant_id.libelle + '/' + self.libelle


class Electronique(models.Model):
    materials = models.ForeignKey(Materiels, verbose_name=("materiel"), on_delete=models.CASCADE)
    numero_serie = models.CharField(verbose_name=("Nom du matériel"), max_length=50, null=True, blank=True, unique=True)
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


#class Vehicule(models.Model):
class Vehicule(models.Model):
    TYPE_TRANSMISSION = (
        ('1', 'Manuel'),
        ('2', 'Automatique'),
    )
    ETAT_VEHICULE = (
        ('1', 'BON ETAT'),
        ('2', 'EN PANNE'),
    )
    materials = models.ForeignKey(Materiels, verbose_name=("materiel"), on_delete=models.CASCADE)
    immatriculation = models.CharField(verbose_name=("Immatriculation Vehicule"), max_length=50, unique=True)
    last_kilometrage = models.IntegerField(verbose_name=("Dernier kilometrage Vehicule (Km/Milles)"), null=True,
                                           blank=True, default=0)
    num_chassi = models.CharField(verbose_name=("Numero de Chassi Vehicule"), max_length=50, null=True,blank=True)
    couleur = models.CharField(verbose_name=("Couleur du Vehicule"), max_length=50, null=True,blank=True)
    # nbre_roue = models.IntegerField(verbose_name=("Nombre de Roue Vehicule"), max_length=50)
    nbre_porte = models.IntegerField(verbose_name=("Nombre de Porte Vehicule"), default=5)
    type_transmissin = models.CharField(max_length=1, choices=TYPE_TRANSMISSION, null=True,blank=True)
    status = models.CharField(max_length=1,verbose_name=("Etat du Vehicule"), choices=ETAT_VEHICULE, null=True,blank=True)
    nbre_chevaux = models.IntegerField(verbose_name=("Nombre de cheveaux"),null=True,blank=True)
    puissance_fiscal = models.IntegerField(verbose_name=("Puissance"),null=True,blank=True)

    type_energie_id = models.ForeignKey(TypeEnergieVehicule, verbose_name=("Type d'Energie"), on_delete=models.CASCADE)
    Typevehicule = models.ForeignKey(Typevehicule, verbose_name=("Type de Véhicule"), on_delete=models.CASCADE)
    model_id = models.ForeignKey(Model, verbose_name=("Model"), on_delete=models.CASCADE)

    @property
    def set_name(self, value):
        self.name = self.immatriculation

    @property
    def get_name(self, value):
        return self.name

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


class Vetement(models.Model):
    taille = models.CharField(verbose_name=("Taille Vetement"), max_length=50)
    couleur = models.CharField(verbose_name=("Couleur Vetement"), max_length=50)
    materiel_utilisé = models.CharField(verbose_name=("Materiel Utilisé"), max_length=50)
    type_vetement_id = models.ForeignKey(TypeVetement, verbose_name=("type vetement"), on_delete=models.CASCADE)
    taille_id = models.ForeignKey(TailleVetement, verbose_name=("taille vetement"), on_delete=models.CASCADE)
    materials = models.ForeignKey(Materiels, verbose_name=("materiel"), on_delete=models.CASCADE)


class Structure(models.Model):
    name = models.CharField(verbose_name=("Libelle"), max_length=50)
    adresse = models.CharField(verbose_name=("adresse"), max_length=50, null=True, blank=True)
    Tel = models.CharField(verbose_name=("tel"), max_length=50, null=True, blank=True)
    structureParent = models.ForeignKey('self', null=True, blank=True, related_name='structureEnfant',
                                        on_delete=models.CASCADE)
    materielStock = models.ManyToManyField(Materiels, through='StructureStock')

    class Meta:
        verbose_name = ("Structure Administrative")
        verbose_name_plural = ("Structures Administrative")

    def __str__(self):
        return self.name


class StructureStock(models.Model):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)
    materiel = models.ForeignKey(Materiels, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    quantite = models.CharField(max_length=64)


class BonCommande(models.Model):
    numero = models.CharField(verbose_name=("Libelle"), max_length=50)
    structure_id = models.ForeignKey(Structure, verbose_name=("structure"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Bon de Commande")
        verbose_name_plural = ("Bons de Commande")

    def __str__(self):
        return self.numero


class BonCommandeDetail(models.Model):
    materiel = models.ForeignKey(Materiels, verbose_name=("designation"), on_delete=models.CASCADE)
    qte = models.CharField(verbose_name=("Quantité"), max_length=50)
    bonCommande = models.ForeignKey(BonCommande, verbose_name=("bon de commande"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Bon de Commande")
        verbose_name_plural = ("Bons de Commande")


class Site(models.Model):
    ETAT = (
        ('OUVERT', 'OUVERT'),
        ('FERMER', 'FERMER'),
    )
    libelle = models.CharField(verbose_name=("Nom du site "), max_length=50)
    description = models.TextField(verbose_name=("Description"), max_length=50, null=True, blank=True)
    Adresse = models.TextField(verbose_name=("adresse"), max_length=50, null=True, blank=True)
    Tel = models.CharField(verbose_name=("Téléphone"), max_length=50, null=True, blank=True)
    gps = models.CharField(verbose_name=("Cordonnée GPS"), max_length=50, null=True, blank=True)
    fax = models.CharField(verbose_name=("Fax"), max_length=50, null=True, blank=True)
    code_postal = models.CharField(verbose_name=("Code Postal"), max_length=10, null=True, blank=True)
    ville = models.CharField(verbose_name=("Ville"), max_length=10)
    pays = models.ForeignKey(Pays, verbose_name=("Pays"), null=True, blank=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name=("Site Parent "), null=True, blank=True,
                               related_name='EntrepotEnfant',
                               on_delete=models.CASCADE)
    etat = models.CharField(max_length=10, choices=ETAT, default='OUVERT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.libelle


class Entrepots(models.Model):
    reference = models.CharField(verbose_name=("Reférence"), max_length=50)
    libelle = models.CharField(verbose_name=("Nom court du lieu"), max_length=50)
    description = models.TextField(verbose_name=("Description"), max_length=50, null=True, blank=True)
    Adresse = models.TextField(verbose_name=("adresse"), max_length=50, null=True, blank=True)
    Tel = models.CharField(verbose_name=("Téléphone"), max_length=50, null=True, blank=True)
    fax = models.CharField(verbose_name=("Fax"), max_length=50, null=True, blank=True)
    parent = models.ForeignKey('self', verbose_name=("Entrepot/Bureau Parent"), null=True, blank=True,
                               related_name='EntrepotEnfant',
                               on_delete=models.CASCADE)
    site = models.ForeignKey(Site, verbose_name=("Site"), related_name='site',
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Bureau")
        verbose_name_plural = ("Bureau")

    def __str__(self):
        return self.libelle


class BonLivraison(models.Model):
    numero = models.CharField(verbose_name=("reference"), max_length=50)
    entrepot_id = models.ForeignKey(Entrepots, verbose_name=("Bureau /Entrepots"), on_delete=models.CASCADE)
    numBonCmd = models.CharField(verbose_name=("Numero de Bon de commande"), max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Stock")
        verbose_name_plural = ("Bons de Livraison")

    def __str__(self):
        return self.numero


class BonLivraisonDetail(models.Model):
    materiel = models.ForeignKey(Materiels, verbose_name=("designation"), on_delete=models.CASCADE)
    qte = models.CharField(verbose_name=("Quantité"), max_length=50)
    bonCommande = models.ForeignKey(BonLivraison, verbose_name=("bon de livraison"), on_delete=models.CASCADE,
                                    null=True, blank=True)
    etatMateriel = models.ForeignKey(EtatMateriel, verbose_name=("Etat"), on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Bon de Commande")
        verbose_name_plural = ("Bons de Commande")

    def __str__(self):
        return self.qte


class stock(models.Model):
    materiel = models.ForeignKey(Materiels, verbose_name=("designation"), on_delete=models.CASCADE)
    entrepot_id = models.ForeignKey(Entrepots, verbose_name=("Entrepots"), on_delete=models.CASCADE)
    qte = models.IntegerField(verbose_name=("Quantité"))
    etatMateriel = models.ForeignKey(EtatMateriel, verbose_name=("Etat"), on_delete=models.CASCADE, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
