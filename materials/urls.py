"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from . import state
from . import pdf


urlpatterns = [

    path('', views.index, name='index'),
    path('dash/pie', views.dash_pie, name='dash_pie'),
    path('mat/', views.MaterielsListView.as_view(), name='dashboard'),

    path('ajax/loadImage', views.loadImage, name='loadImage'),
    path('vehicule/', views.IndexView.as_view(), name='vehiculeList'),

    path('vehicule/add', views.VehiculeCreate, name='vehiculeAdd'),
    path('vehicule/<int:pk>/edit', views.VehiculeUpdate, name='vehicule.update'),
    path('vehicule/del', views.VehiculeDelete, name='vehicule.delete'),

    path('material/add', views.MaterielsCreate, name='material.Add'),
    path('materiel/', views.MaterielsListView.as_view(), name='materialList'),
    path('materiel/<int:pk>/edit', views.MaterielsUpdate, name='materiel.update'),
    path('materiel/del', views.MaterielDelete, name='materiel.delete'),

    path('etat/', views.Etat, name='etat.search'),
    path('etat/cat', views.EtatCat, name='etat.search_cat'),
    path('print/', views.PrintEtat, name='etat.print'),
    path('pdf/', state.pdf_par_site, name='etat.pdf'),
    path('pdf/filter', state.pdf_filter, name='etat.pdf_filter'),
    path('pdf/filter/cat', state.cat_pdf_filter, name='etat.cat_pdf_filter'),


    path('site/add', views.SiteCreate, name='site.Add'),
    path('site/', views.SiteListView.as_view(), name='site'),
    path('site/<int:pk>/edit', views.SiteUpdate, name='site.update'),
    path('site/<int:pk>/detail', views.SiteDetail, name='site.detail'),
    path('site/del', views.SiteDelete, name='site.delete'),


    path('entrepot/add', views.EntrepotCreate, name='entrepot.Add'),
    path('entrepot/stock/add', views.StockEntrepot.as_view(), name='entrepot.AddStock'),
    path('entrepot/', views.EntrepotListView.as_view(), name='entrepotList'),
    path('entrepot/<int:pk>/edit', views.EntrepotUpdate, name='entrepot.update'),
    path('entrepot/<int:pk>/detail', views.EntrepotDetail, name='entrepot.detail'),


]
