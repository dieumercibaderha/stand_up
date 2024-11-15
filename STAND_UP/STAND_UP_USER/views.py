from django.shortcuts import render
from STAND_UP_APP.models import *

from django.template.loader import render_to_string
from STAND_UP import settings
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from django.contrib.auth import get_user_model
from datetime import datetime, date
from django.core.mail import send_mail, EmailMessage
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site

auj=date.today()
# Create your views here.
@login_required
def accueil1(request):
    current_site=get_current_site(request)
    ut=request.user
    context={
        'ut':ut,
        "domain":current_site.domain,
        'ce':Alerte.objects.all().count(),
        'cm':Maladie.objects.filter(id__in=Alerte.objects.values('Maladie')).count(),
        'cu':User.objects.filter(username__in=Alerte.objects.values('Enqueteur')).count(),
        'alerte':Alerte.objects.all(),
        'notif':Alerte.objects.filter(Dates__date=auj),
        
        
    }
    return render(request, "accueil1.html", context)


@login_required
def enregistrement(request):
    return render(request, "error_5001.html")



@login_required
def add_alerte1(request):
    current_site=get_current_site(request)
    ut=request.user
    maladie=Maladie.objects.all()
    if request.method=="POST":
        asc=request.POST.get('ASC')
        zs=request.POST.get('Zone_de_sant')
        maladies=request.POST.get('maladie')
        cas=request.POST.get('Cas')
        
        crea=Alerte.objects.create(
            Enqueteur=f"{ut.username}", 
            Photo=ut.Photo,
            Maladie=Maladie.objects.get(id=maladies),
            Cas=cas,
            ASC=asc,
            Zone_de_sant=zs,
            
            Province=ut.Lieu
        )
        try:
            us=User.objects.all()
            subject="SURVEILLANCE JOURNALIERE BASEE SUR LES EVENEMENTS(SBE)"
            message=f"""Le système d'alerte des cas de maladie à potentiel épidemique vient d'enregistrer ce jour :\n
            -CAS: {cas}
            -MALADIE: {Maladie.objects.get(id=maladies)}
            -LOCALITE: {ut.Lieu}
            -RECO: {ut.Nom}
            """
            from_email=settings.EMAIL_HOST_USER
            l=["baderha1@gmail.com"]
            l.extend([li.email for li in us])
            to_list=l
            send_mail(subject, message, from_email, l, fail_silently=False)
            
            crea.save()
            
            return redirect('enregistrement')
        except:
            return render(request, "error_4001.html")
    context={
        'ut':ut,
        'maladie':maladie,
        'alertes':Alerte.objects.all(),
        'notif':Alerte.objects.filter(Dates=auj),
        "domain":current_site.domain,
        'notif':Alerte.objects.filter(Dates__date=auj),
        
        
    }
    
    return render(request, "add_alerte1.html", context)

@login_required
def compte1(request, id):
    current_site=get_current_site(request)
    ut=request.user
    compteuser=User.objects.get(id=id)
    menquete=Alerte.objects.filter(Enqueteur=ut.username)
    
    context={
        'compteuser':compteuser,
        'ut':request.user,
        "domain":current_site.domain,
        'menquete':menquete,
        'notif':Alerte.objects.filter(Dates__date=auj),
    }
    return render(request, "compte1.html", context)