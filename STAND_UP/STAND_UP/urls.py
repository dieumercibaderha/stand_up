"""
URL configuration for STAND_UP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from STAND_UP_APP.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admine, name="admin"),
    path('logina/', logina, name="logina"),
    path('accounts/login/', loginse, name='logine'),
    path('addalerte/', add_alerte, name="addalerte"),
    path('modalerte/', mod_alerte, name='mod_alerte'),
    path('allerte/', alertes, name='allerte'),
    path('listes_agents', list_agents, name='list_agents') ,
    path('', accueil, name="accueil"),
    path('compte/<str:id>', compte, name="compte"),
    path('profile_agents/<str:id>', profil_agents, name="profile_agents"),
    path('register', registe, name="register"),
    path('deconnexion/', deconnexion, name="deconnexion"),
    path('impression', affiche, name='imprimer'),
    path('modifier/', modifier, name='modifier'),
    path('supp/<str:id>', supp, name="supp"),
    path('list_maladie', list_maladies, name="list_maladie"),
    path('addmaladie/', add_maladie, name="addmaladie"),
    path('modmaladie/<str:id>', mod_maladie, name="mod_maladie"),
    path('suppmaladie/<str:id>', supp_maladie, name="sup_maladie"),
    path('addorgan/', add_Organ, name="addorgan"),
    path('modorgan/<str:id>', mod_Organ, name="modorgan"),
    path('supporgan/<str:id>', supp_Organ, name="sup_organ"),
    path('Organ/', organ, name="organ"),
    path('enqueteur/', include("STAND_UP_USER.urls"), name="STAND_UP_USER"),
    path('addagents/', add_agents, name="addagents"),
    
    path('api/list_alerte/', AlerteListCreate.as_view(), name='mymodel-list-create'), 
    path('api/alerte_detail/<int:pk>/', AlerteDetail.as_view(), name='mymodel-detail'),
    
    path('api/list_maladie/', MaladieListCreate.as_view(), name='MaladieListCreate'), 
    path('api/maladie_detail/<int:pk>/', MaladieDetail.as_view(), name='maladie-detail'),
    
    path('api/list_user/', UserListCreate.as_view(), name='user-list-create'), 
    path('api/user_detail/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
