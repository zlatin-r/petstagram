from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from petstagram.accounts.forms import AppUserCreationForm, ProfileEditForm
from petstagram.accounts.models import Profile

UserModel = get_user_model()


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return response


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'


# def profile_details(request, pk):
#     return render(request, template_name='accounts/profile-details-page.html')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # better way to take all likes:
        photos_with_likes = self.object.photo_set.annotate(likes_count=Count('like'))

        context['total_likes_count'] = sum(p.like_set.count() for p in self.object.photo_set.all())
        context['total_pets_count'] = self.object.pet_set.count()
        context['total_photos_count'] = self.object.photo_set.count()

        return context


# def delete_profile(request, pk):
#     return render(request, template_name='accounts/profile-delete-page.html')


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        # check if it's the logged user, if not raises error
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def test_func(self):
        # check if it's the logged user, if not raises error
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.object.pk,
            }
        )
