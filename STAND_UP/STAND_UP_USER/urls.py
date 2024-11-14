from django.urls import path
from .views import *

urlpatterns = [
    path('indexs', add_alerte1, name="indexs"),
    path('compte1/<str:id>', compte1, name="compte1"),
    path('', accueil1, name="accueil1"),
    path('enregistrement/', enregistrement, name="enregistrement")
    
]