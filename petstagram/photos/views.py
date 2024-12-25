from django.shortcuts import render

# Create your views here.
def photo_add(request):
    return render(request, template_name='photos/photo-add-page.html')

def photo_details(request):
    return render(request, template_name='photos/photo-details-page.html')

def photo_edit(request):
    return render(request, template_name='photos/photo-edit-page.html')