from django.views.generic import TemplateView
from .forms import PetForm, PersonForm
from .models import Person, Pet
from multiviewniverse.core.views import MultiModelCreateFormView, MultiModelUpdateFormView


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['people'] = Person.objects.all()
        return context


class CreatePersonPetView(MultiModelCreateFormView):
    model_form_classes = [(PetForm, Pet), (PersonForm, Person)]
    template_name = 'person_pet_form.html'
    success_url = '/'


class UpdatePersonPetView(MultiModelUpdateFormView):
    model_form_classes = [(PersonForm, Person), (PetForm, Pet)]
    template_name = 'person_pet_form.html'
    success_url = '/'

    def get_person_object(self):
        return Person.objects.get(pk=self.kwargs['person_pk'])

    def get_pet_object(self):
        return self.get_person_object().pets.get(pk=self.kwargs['pet_pk'])
