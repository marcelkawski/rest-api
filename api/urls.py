from django.urls import path
from . import views

urlpatterns = [
    path('', views.PhotoAllView.as_view()),
    path('<int:photo_id>', views.PhotoDetailView.as_view()),
]
