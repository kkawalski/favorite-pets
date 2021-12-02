from django import forms

from core.models import Animal, AnimalImage


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = [
            "name",
            "color",
            "kind",
            "owner",
        ]


class AnimalImageForm(forms.ModelForm):
    class Meta:
        model = AnimalImage
        fields = [
            "url",
            "kind",
            "user",
            "file_type",
        ]

