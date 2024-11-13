from django.urls import path
from .views import *

urlpatterns = [
    path('indexs', add_alerte, name="indexs"),
    path('compte1/<str:id>', compte, name="compte1"),
    path('', accueil, name="accueil1"),
    path('enregistrement/', enregistrement, name="enregistrement")
    
]