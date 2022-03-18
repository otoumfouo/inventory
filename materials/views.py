from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, request, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from formtools.wizard.views import WizardView
from django.contrib import messages
# Create your views here.
from .forms import *
from .models import *
from django.db.models import Avg, Count, Min, Sum
from django.views.generic.detail import SingleObjectMixin
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from reportlab.lib.utils import StringIO
from math import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
'''USER PASSWORD CHANGE'''

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Le mot de Passe a été bien modifié ')
            return redirect('change_password')
        else:
            messages.error(request, 'Veuillez corriger les différentes erreurs.')
    else:
        current_user = request.user
        #user = User.objects.filter(pk=current_user.id).first()
        #return HttpResponse(current_user.email)
        form = PasswordChangeForm(request.user)
        #userform = UserForm(request.user)
    return render(request, 'registration/change_pass.html', locals())
''' TABLEAU DE BORD'''
@login_required
def index(request):
    materiels_list = Materiels.objects.all()
    TotalMateriel = stock.objects.all().aggregate(Sum("qte"))
    Total = 0  if  TotalMateriel['qte__sum']==None else TotalMateriel['qte__sum']
    nbre_sites = Site.objects.count()
    sites = Site.objects.all()
    site_info = []
    for site in sites:
        value = stock.objects.filter(entrepot_id__site=site).aggregate(Sum("qte"))
        site_info.append({"label": site.libelle, "nbre": 0  if  value['qte__sum']==None else value['qte__sum']})
    if nbre_sites == 0:
        nbre_cellule = 12-1
    else:
        nbre_cellule = ceil(12/nbre_sites)-1
    entrepots =  Entrepots.objects.all().order_by('id')[:3]

    #TotalMateriel = stock.objects.filter(entrepot_id__site=site).aggregate(Sum("qte"))
    return render(request, "dashbord.html", locals())

@login_required
def dash_pie(request):
    # def dash_pie(request, start, end):
    sites = Site.objects.all()
    label = []
    series = []
    data = []
    for site in sites:

        #value = ent.stock_set.all().aggregate(Sum("qte"))
        value = stock.objects.filter(entrepot_id__site=site).aggregate(Sum("qte"))
        '''value = Alert.objects.filter(source_information=source)\
            .filter(datedebut__range=[start, end])\
            .count()'''
        #series.append((value['qte__sum'])value_if_true if not myString: else value_if_false
        #val =
        series.append(0  if  value['qte__sum']==None else value['qte__sum'])
        label.append(site.libelle)
    data.append({"label": label, "series": series})

    return JsonResponse(data, safe=False)


'''
gestion des Sites
'''


class SiteListView(ListView):
    template_name = 'rakuda/sites/index.html'
    context_object_name = 'sites_List'

    def get_queryset(self):
        return Site.objects.all()

@login_required
def SiteCreate(request):
    siteForm = SitesForm(request.POST or None, request.FILES or None)
    print(siteForm)
    if siteForm.is_valid():
        new_ent = siteForm.save()
        new_ent.save()
        messages.success(request, "L'entrepot a été bien Enregistré'")
        return redirect("site")

    return render(request, "rakuda/sites/forms.html", locals())

@login_required
def SiteUpdate(request, pk):
    entrepots = get_object_or_404(Site, pk=pk)
    Entform = SitesForm(request.POST or None, request.FILES or None, instance=entrepots)

    if Entform.is_valid():
        Entform.save()
        messages.success(request, "l'entrepot a été bien Modifier")
        return redirect("entrepotList")

    return render(request, "rakuda/sites/forms.html", locals())

@login_required
def SiteDelete(request):
    site = get_object_or_404(Site, pk=request.POST.get("pk"))
    site.delete()
    return redirect("site")

@login_required
def SiteDetail(request, pk):
    # site = get_object_or_404(Site, pk=pk)
    site = get_object_or_404(Site, pk=pk)

    entrepots = Entrepots.objects.filter(site__pk=site.id)

    print(entrepots)
    entrepot = Entrepots.objects.all()
    for ent in entrepot:
        print(ent.stock_set.all().aggregate(Sum("qte")))

    return render(request, "rakuda/sites/detail.html", locals())


'''
gestion des entrepots
'''


class EntrepotListView(ListView):
    template_name = 'rakuda/entrepots/index.html'
    context_object_name = 'entrepots_List'

    def get_queryset(self):
        return Entrepots.objects.all()

@login_required
def EntrepotCreate(request):
    Entform = EntrepotsForm(request.POST or None, request.FILES or None)

    if Entform.is_valid():
        new_ent = Entform.save()
        new_ent.save()
        messages.success(request, "L'entrepot a été bien Enregistré'")
        return redirect("entrepotList")

    return render(request, "rakuda/entrepots/form.html", locals())

@login_required
def EntrepotUpdate(request, pk):
    entrepots = get_object_or_404(Entrepots, pk=pk)
    Entform = EntrepotsForm(request.POST or None, request.FILES or None, instance=entrepots)

    if Entform.is_valid():
        Entform.save()
        messages.success(request, "l'entrepot a été bien Modifier")
        return redirect("entrepotList")

    return render(request, "rakuda/entrepots/form.html", locals())

@login_required
def EntrepotDetail(request, pk):
    site = get_object_or_404(Entrepots, pk=pk)
    total = site.stock_set.aggregate(Sum('qte'))
    # print(total)
    return render(request, "rakuda/entrepots/detail.html", locals())


class StockEntrepot(CreateView):
    model = BonLivraison
    # company_name = forms.ImageField()
    # fields = ('NumRequisition', 'DateArrive', 'Operateur', 'StartDate', 'EndDate', 'Investigator', 'company_name')
    fields = '__all__'
    # form_class = BonLivraisonForm
    template_name = 'rakuda/entrepots/bon-livraison.html'
    # extra_context = {"register_form": InvestigatorForm}
    success_url = reverse_lazy('requisition.index')

    # print(form_class)
    def get_context_data(self, **kwargs):
        data = super(StockEntrepot, self).get_context_data(**kwargs)
        if self.request.POST:
            print("POST REQUEST")
            data['detail'] = RequistionRequestFormSet(self.request.POST, self.request.FILES,
                                                      instance=self.object, prefix="form_set")
        else:
            data['detail'] = RequistionRequestFormSet(instance=self.object, prefix="form_set")
        return data

    def form_valid(self, form):
        print("debut execusion")
        context = self.get_context_data()
        bondetail = context['detail']

        with transaction.atomic():

            if bondetail.is_valid():
                self.object = form.save()
                nbre = int(self.request.POST.get("form_set-TOTAL_FORMS"))
                print(type(nbre))

                bondetail.instance = self.object
                bondetail.save()

                for i in range(0, nbre):
                    print(i)
                    materielFiel = "form_set-" + str(i) + "-materiel"
                    QteField = "form_set-" + str(i) + "-qte"
                    mat = self.request.POST.get(materielFiel)
                    qte = self.request.POST.get(QteField)
                    qte = self.request.POST.get(QteField)
                    entrepot = int(self.request.POST.get("entrepot_id"))
                    print(mat)
                    print(qte)
                    if nbre and qte:
                        print(stock.objects.filter(materiel__pk=mat).filter(entrepot_id__pk=entrepot).count())
                        if stock.objects.filter(materiel__pk=mat).filter(entrepot_id__pk=entrepot).count() != 0:
                            ligne = stock.objects.filter(materiel__pk=mat).filter(entrepot_id__pk=entrepot).get()
                            ligne.qte = int(ligne.qte) + int(qte)
                        else:
                            stocks = stock.objects.create(
                                materiel=Materiels.objects.get(pk=mat),
                                entrepot_id=Entrepots.objects.get(pk=entrepot),
                                qte=qte,
                            )
                            stocks.save()

                messages.success(self.request, "La requisition Numéro  " + str(
                    self.request.POST.get("NumRequisition")) + " a été ajoutée avec Success")
                return redirect("entrepotList")
                # return HttpResponseRedirect(self.get_success_url())
            else:
                print("erreurs")
                return super().form_invalid(form)

    def form_invalid(self, form):
        print("form is invalid")
        return super().form_invalid(form)


'''
gestion des materiels
'''


class MaterielsListView(ListView):
    template_name = 'rakuda/materiels/index.html'
    context_object_name = 'materiels_list'

    def get_queryset(self):
        return Materiels.objects.all()

@login_required
def MaterielsCreate(request):
    Matform = MaterielsForm(request.POST or None, request.FILES or None)

    if Matform.is_valid():
        new_materiel = Matform.save()
        new_materiel.save()
        messages.success(request, "Le matériel a été bien Enregistré'")
        return redirect("materialList")

    return render(request, "rakuda/materiels/form.html", locals())

@login_required
def MaterielsUpdate(request, pk):
    materiels = get_object_or_404(Materiels, pk=pk)
    Matform = MaterielsForm(request.POST or None, request.FILES or None, instance=materiels)

    if Matform.is_valid():
        Matform.save()
        messages.success(request, "le matériel a été bien Modifier")
        return redirect("materialList")

    return render(request, "rakuda/materiels/form.html", locals())

@login_required
def MaterielDelete(request):
    mat = get_object_or_404(Materiels, pk=request.POST.get("pk"))
    mat.delete()
    return redirect("materialList")

@login_required
def VehiculeCreate(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VehiculeForm(request.POST)
        Matform = MaterielsVehiculeForm(request.POST)
        ##
        #print()
        #print(Matform)
        #return HttpResponse(Matform.is_valid())
        # check whether it's valid:
        if Matform.is_valid() and form.is_valid():
        #if  form.is_valid():
            #return HttpResponse(form)
            new_materiel = Matform.save(commit=False)
            new_materiel.name = request.POST.get('immatriculation')
            #new_materiel.type = CategorieMateriel.objects.get(pk=6)
            new_materiel.type = CategorieMateriel.objects.get(pk=6)
            new_materiel.en_stock = True
            new_materiel.save()
            new_vehicule = form.save(commit=False)
            new_vehicule.materials = new_materiel
            form.save()
            # new_materiel.save()

            messages.success(request, "le Véhicule a été bien enregister")
            return render(request, "rakuda/vehicule/index.html", locals())

        # if a GET (or any other method) we'll create a blank form
    else:
        form = VehiculeForm()

        #return HttpResponse(form)
        # context['form'] = VehiculeForm()
        Matform = MaterielsVehiculeForm()
        # print(Matform.fabricat_year)
    return render(request, "rakuda/vehicule/forms.html", context={'form': form, 'Matform': Matform})

@login_required
def VehiculeUpdate(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    form = VehiculeForm(request.POST or None, request.FILES or None, instance=vehicule)
    Matform = MaterielsVehiculeForm(request.POST or None, request.FILES or None, instance=vehicule.materials)

    if Matform.is_valid() and form.is_valid():
        new_materiel = Matform.save()
        new_materiel.name = request.POST.get('immatriculation')
        new_materiel.save()
        new_vehicule = form.save(commit=False)
        new_vehicule.materials = new_materiel
        form.save()
        messages.success(request, "le Véhicule a été bien Modifier")
        return redirect("vehiculeList")

    return render(request, "rakuda/vehicule/forms.html", locals())

@login_required
def VehiculeDelete(request):
    vehicule = get_object_or_404(Vehicule, pk=request.POST.get("pk"))
    mat = get_object_or_404(Materiels, pk=vehicule.materials.id)
    mat.delete()
    vehicule.delete()
    return redirect("vehiculeList")
@login_required
def dashboard(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VehiculeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_vehicule = form.save()

            return render(request, "rakuda/index.html", locals())

        # if a GET (or any other method) we'll create a blank form
    else:
        form = VehiculeForm()
        # context['form'] = VehiculeForm()

        Materielsform = MaterielsForm()

    return render(request, "rakuda/index.html", locals())


class IndexView(ListView):
    template_name = 'rakuda/vehicule/index.html'
    context_object_name = 'vehicule_list'

    def get_queryset(self):
        return Vehicule.objects.all()

@login_required
class ContactDetailView(DetailView):
    model = Vehicule
    template_name = 'vehicule/vehicule-detail.html'


def loadImage(request):
    model_id = request.GET.get("id")
    model = Model.objects.filter(pk=model_id).get()
    image = model.fabricant_id.image
    data = {"image": str(model.fabricant_id.image)}

    return JsonResponse(data, safe=False)


''' GESTION DES ETATS '''

@login_required
def Etat(request):
    form = SearchForm(request.POST or None, request.FILES or None, )
    return render(request, "rakuda/etat/etat.html", locals())

@login_required
def EtatCat(request):
    form = SearchCatForm(request.POST or None, request.FILES or None, )
    return render(request, "rakuda/etat/etat_categorie.html", locals())

@login_required
def PrintEtat(request):
    form = SearchForm(request.POST or None, request.FILES or None, )
    if request.POST or request.GET:
        print(request.POST.get("bureau"))
        entrepot = Entrepots.objects.filter(pk=request.GET.get("bureau")).get()
        context = {'site': entrepot}
        template = get_template('rakuda/etat/print_bureau.html')
        html = template.render(context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        print(entrepot)
        if not pdf.err:
            # print(result.getvalue())
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None
    return render(request, "rakuda/etat/etat.html", locals())

@login_required
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    if not pdf.err:
        print(result.getvalue())
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def etatPdf(request):
    if request.POST:
        entrepot = Entrepots.objects.filter(pk=request.POST.get("bureau"))
        pdf = render_to_pdf('civis/cork/printExtrait.html', data)


class ViewPDF(View):
    def get(self, request, id, *args, **kwargs):
        pdf = render_to_pdf('civis/cork/printExtrait.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('app/pdf_template.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
