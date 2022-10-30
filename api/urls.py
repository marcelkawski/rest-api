from django.urls import path
from . import views

urlpatterns = [
    path('', views.RESTAPIView.as_view(), name='all')
]
