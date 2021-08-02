from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from formtools.wizard.views import WizardView

# Create your views here.
from materials.forms import VehiculeForm
from .models import *


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

    return render(request, "rakuda/index.html", locals())


class IndexView(ListView):
    template_name = 'rakuda/vehicule/index.html'
    context_object_name = 'vehicule_list'

    def get_queryset(self):
        return Vehicule.objects.all()


class ContactDetailView(DetailView):
    model = Vehicule
    template_name = 'vehicule/vehicule-detail.html'


def loadImage(request):
    model_id = request.GET.get("id")
    model = Model.objects.filter(pk=model_id).get()
    image = model.fabricant_id.image
    data = {"image": str(model.fabricant_id.image)}

    return JsonResponse(data, safe=False)
