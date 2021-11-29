from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse

from core.forms import AnimalForm
from core.models import Animal


class HomeView(TemplateView):
    template_name = "home.html"


class AnimalsListView(ListView):
    model = Animal
    template_name = "animals_list.html"


class AnimalCreateView(CreateView):
    model = Animal
    # form_class = AnimalForm
    template_name = "animals_create.html"
    success_url = reverse_lazy('animal-list')
    fields = ("kind", "name", 'color')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
