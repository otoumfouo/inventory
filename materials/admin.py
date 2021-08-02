from django.contrib import admin
from .models import *

# Register your models here.
"""@admin.register(Materiels)
class MaterielAdmin(admin.ModelAdmin):
    pass"""
@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    pass
@admin.register(Vetement)
class VetementAdmin(admin.ModelAdmin):
    pass
@admin.register(TailleVetement)
class TailleVetementAdmin(admin.ModelAdmin):
    pass
@admin.register(TypeVetement)
class TypeVetementAdmin(admin.ModelAdmin):
    pass
@admin.register(Typevehicule)
class TypevehiculeAdmin(admin.ModelAdmin):
    pass
@admin.register(TypeEnergieVehicule)
class TypeEnergieVehiculeAdmin(admin.ModelAdmin):
    pass

class ModelInline(admin.TabularInline):
    model = Model


@admin.register(Fabricant)
class FabricantAdmin(admin.ModelAdmin):
    inlines = [ModelInline]

