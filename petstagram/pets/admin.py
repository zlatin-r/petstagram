from django.contrib import admin

from petstagram.pets.models import Pet


# Register your models here.

@admin.register(Pet)
class Pet(admin.ModelAdmin):
    list_display = ("name", "slug")
