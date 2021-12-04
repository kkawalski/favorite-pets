from django.contrib import admin

from core.models import Animal, AnimalImage, User


admin.site.register(Animal)
admin.site.register(AnimalImage)
admin.site.register(User)
