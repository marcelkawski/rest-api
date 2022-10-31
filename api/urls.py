from django.urls import path
from . import views

urlpatterns = [
    path('', views.PhotoAllView.as_view()),
    path('<int:photo_id>', views.PhotoDetailView.as_view()),
    path('import-data-api', views.import_data_from_api),
    path('import-data-json', views.import_data_from_json)
]
