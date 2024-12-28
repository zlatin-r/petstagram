from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from petstagram.common.forms import CommentForm
from petstagram.pets.forms import PetForm, PetDeleteForm
from petstagram.pets.models import Pet


# Create your views here.

# def pet_add(request):
#     form = PetForm(request.POST or None)
#
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('profile-details', pk=1)
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'pets/pet-add-page.html', context)

class AddPetView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet-add-page.html'
    success_url = reverse_lazy('profile-details', kwargs={'pk': 1})


def pet_details(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    all_photos = pet.photo_set.all()
    comment_form = CommentForm()

    context = {
        'pet': pet,
        'all_photos': all_photos,
        'comment_form': comment_form,
    }

    return render(request, 'pets/pet-details-page.html', context)


def pet_edit(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    form = PetForm(request.POST or None, instance=pet)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('pet-details', username, pet_slug)

    context = {
        'form': form,
        'pet': pet,
    }

    return render(request, 'pets/pet-edit-page.html', context)


def pet_delete(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    form = PetDeleteForm(instance=pet)

    if request.method == 'POST':
        pet.delete()
        return redirect('profile-details', pk=1)

    context = {
        'form': form,
    }
    return render(request, 'pets/pet-delete-page.html', context)
