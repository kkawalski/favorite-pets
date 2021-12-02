from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy, reverse

from core.forms import AnimalForm, AnimalImageForm
from core.models import Animal, AnimalImage


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


class AnimalImageInitView(FormView):
    form_class = AnimalImageForm
    template_name = "image_save.html"
    success_url = reverse_lazy('get-animal')

    def get_context_data(self, **kwargs):
        print('gET', self.request.GET)
        kind = self.request.GET.get('type', '')
        animal_image = AnimalImage.get_image(kind, self.request.user)
        kwargs['animal_image'] = animal_image
        return super().get_context_data(**kwargs)

    def get_initial(self):
        kind = self.request.GET.get('type', '')
        animal_image = AnimalImage.get_image(kind, self.request.user)
        return {'url': animal_image.url,
                'kind': animal_image.kind, 
                'user': animal_image.user, 
                'file_type': animal_image.file_type}

    def post(self, request, *args: str, **kwargs):
        print(self.request.POST)
        return super().post(request, *args, **kwargs)
