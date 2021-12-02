from django.urls import path

from core.views import HomeView, AnimalsListView, AnimalCreateView, AnimalImageInitView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('animals/', AnimalsListView.as_view(), name='animal-list'),
    path('animals/create/', AnimalCreateView.as_view(), name='animal-create'),
    path('animal-image/', AnimalImageInitView.as_view(), name='get-animal'),
]
