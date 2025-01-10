from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

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

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.user = self.request.user       # attach the new pet to the current user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.request.user.pk,
            }
        )


# def pet_details(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     all_photos = pet.photo_set.all()
#     comment_form = CommentForm()
#
#     context = {
#         'pet': pet,
#         'all_photos': all_photos,
#         'comment_form': comment_form,
#     }
#
#     return render(request, 'pets/pet-details-page.html', context)


class PetDetailsView(DetailView):
    model = Pet
    template_name = 'pets/pet-details-page.html'
    context_object_name = 'pet'
    slug_url_kwarg = 'pet_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_photos'] = self.object.photo_set.all()
        context['comment_form'] = CommentForm()
        return context


# def pet_edit(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetForm(request.POST or None, instance=pet)
#
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('pet-details', username, pet_slug)
#
#     context = {
#         'form': form,
#         'pet': pet,
#     }
#
#     return render(request, 'pets/pet-edit-page.html', context)


class EditPetView(UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet-edit-page.html'
    slug_url_kwarg = 'pet_slug'
    context_object_name = 'pet'

    def get_success_url(self):
        return reverse_lazy(
            'pet-details',
            kwargs={
                'username': self.kwargs['username'],
                'pet_slug': self.kwargs['pet_slug']
            })


# def pet_delete(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetDeleteForm(instance=pet)
#
#     if request.method == 'POST':
#         pet.delete()
#         return redirect('profile-details', pk=1)
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'pets/pet-delete-page.html', context)


class DeletePetView(DeleteView):
    model = Pet
    template_name = 'pets/pet-delete-page.html'
    slug_url_kwarg = 'pet_slug'
    form_class = PetDeleteForm
    success_url = reverse_lazy('profile-details', kwargs={'pk': 1})

    # context_object_name = 'pet'

    def get_initial(self):
        return self.get_object().__dict__

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'data': self.get_initial(),
        })

        return kwargs

    # def get_object(self, queryset=None):
    #     return Pet.objects.get(slug=self.kwargs['pet_slug'])
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = PetDeleteForm(initial=self.object.__dict__)
    #     return context
    #
    # def delete(self, request, *args, **kwargs):
    #     pet = self.get_object()
    #     pet.delete()
    #     return redirect(self.success_url)
