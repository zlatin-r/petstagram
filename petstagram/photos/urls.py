from django.urls import path, include

from petstagram.photos import views

urlpatterns = [
    path('add/', views.photo_add, name='photo-add'),
    path('<int:pk>/', include([
        path('', views.photo_details, name='photo-details'),
        path('edit/', views.photo_edit, name='photo-edit'),
    ])),
]
