from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy

from petstagram.common.forms import CommentForm, SearchForm
from petstagram.common.models import Like
from petstagram.photos.models import Photo


# Create your views here.
def index(request):
    all_photos = Photo.objects.all()
    comment_form = CommentForm()
    search_form = SearchForm(request.GET)

    if search_form.is_valid():
        all_photos = all_photos.filter(
            tagged_pets__name__icontains=search_form.cleaned_data['pet_name'],
        )

    photos_per_page = 1
    paginator = Paginator(all_photos, photos_per_page)
    page = request.GET.get('page')

    try:
        all_photos = paginator.get_page(page)
    except PageNotAnInteger:
        all_photos = paginator.page(1)
    except EmptyPage:
        all_photos = paginator.get_page(paginator.num_pages)

    context = {
        'all_photos': all_photos,
        'comment_form': comment_form,
        'search_form': search_form,
    }

    return render(request, 'common/home-page.html', context)


def like_functionality(request, photo_id: int):
    liked_object = Like.objects.filter(to_photo_id=photo_id)

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo_id=photo_id)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")


def copy_link_to_clipboard(request, photo_id: int):
    copy(request.META['HTTP_HOST'] + resolve_url('photo-details', photo_id))

    return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")


def add_comment(request, photo_id: int):
    if request.method == 'POST':
        photo = Photo.objects.get(pk=photo_id)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_photo = photo
            comment.save()

        return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")
