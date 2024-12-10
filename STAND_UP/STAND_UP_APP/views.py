
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
from django.utils import timezone
from rest_framework import generics
from .serializers import *
auj=timezone.now().date()
User = get_user_model()



class AlerteListCreate(generics.ListCreateAPIView):
    queryset = Alerte.objects.all()
    serializer_class = AlerteSerializer

class AlerteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alerte.objects.all()
    serializer_class = AlerteSerializer
    
    
class MaladieListCreate(generics.ListCreateAPIView):
    queryset = Maladie.objects.all()
    serializer_class = MaladieSerializer

class MaladieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Maladie.objects.all()
    serializer_class = AlerteSerializer


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer






# Create your views here.

def admine(request):
    return redirect('logina')



@login_required
def affiche(request):
    current_site = get_current_site(request) 
    site_url = f"https://{current_site.domain}"
    agents=User.objects.all()
    context={
          'agents':agents,
            'site':site_url
            }
    templates=get_template("agents.html").render(context)
    pdf_file=HTML(string=templates).write_pdf(stylesheets=[CSS(string='''
                                                                            @page{
                                                                                size:A4 landscape;
                                                                                margin-left:0.2cm;
                                                                                margin-top:1.0cm;}
                                                                               
                                                                                '''
                                                                                )])
    response=HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition']='filename="agents.pdf'
    return response 
     
        




@login_required
def accueil(request):
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
    return render(request, "accueil.html", context)

@login_required
def add_maladie(request):
    current_site=get_current_site(request)
    ut=request.user
    maladie=Maladie.objects.all()
    if request.method=="POST":
        
        maladies=request.POST.get('nom')
        
        
        crea=Maladie.objects.create(
            Nom=maladies
        )
        crea.save()
        
        
        return redirect('list_maladie')
    context={
        'ut':ut,
       
       
        'notif':Alerte.objects.filter(Dates__date=auj),
      
        
        
    }
    
    return render(request, "add_maladie.html", context)


@login_required
def mod_maladie(request, id):
    ut=request.user
    maladie=Maladie.objects.get(id=id)
    if request.method=="POST":
        
        maladies=request.POST.get('nom')
        
        
        maladie.Nom=maladies
        maladie.save()
        
        
        return redirect('list_maladie')
    context={
        'ut':ut,
        'notif':Alerte.objects.filter(Dates__date=auj),
        'maladie':maladie
    }
    
    return render(request, "mod_maladie.html", context)
@login_required
def supp_maladie(request, id):
   
    maladie=Maladie.objects.get(id=id)
       
    maladie.delete()
        
        
    return redirect('list_maladie')

def organ(request):
    ut=request.user
    organs=Organisation.objects.all()
    if request.method=="GET":
        ords=request.GET.get('organ')
        if ords is not None:
            organs=Organisation.objects.filter(Nom__icontains=ords)
   
    context={
        'ut':ut,
        'organs':organs,
        'notif':Alerte.objects.filter(Dates__date=auj),
    }
    
    return render(request, "organ.html", context)    

@login_required
def add_Organ(request):
    
    ut=request.user
    
    if request.method=="POST":
        
        nom=request.POST.get('nom')
        ad=request.POST.get('ad')
        tel=request.POST.get('tel')
        
        
        crea=Organisation.objects.create(
            Nom=nom,
            Adresse=ad,
            Tel=tel
        )
        crea.save()
        
        
        return redirect('organ')
    context={
        'ut':ut,
       
       
        'notif':Alerte.objects.filter(Dates__date=auj),
        
        
    }
    
    return render(request, "add_organ.html", context)




@login_required
def mod_Organ(request, id):
    ut=request.user
    ordg=Organisation.objects.get(id=id)
    if request.method=="POST":
        ids=request.POST.get('id')
        nom=request.POST.get('nom')
        ad=request.POST.get('ad')
        tel=request.POST.get('tel')
        obj=Organisation.objects.filter(id=ids).update(Nom=nom, Adresse=ad)
       
        
        
        return redirect('organ')
    context={
        'ut':ut,
        'orgd':ordg,
       
        'notif':Alerte.objects.filter(Dates__date=auj),
      
        
        
    }
    
    return render(request, "mod_organ.html", context)

@login_required
def supp_Organ(request, id):
   
    organ=Organisation.objects.get(id=id)
       
    organ.delete()
        
        
    return redirect('organ')



@login_required
def add_alerte(request):
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
        
        us=User.objects.all()
        subject="SURVEILLANCE JOURNALIERE BASEE SUR LES EVENEMENTS(SBE)"
        message=f"""Le système d'alerte des cas de maladie à potentiel épidemique vient d'enregistrer ce jour :\n
            -CAS: {cas}
            -MALADIE: {Maladie.objects.get(id=maladies)}
            -LOCALITE: {ut.Lieu}
            -RECO: {ut.Nom}
            """
        l=["baderha@gmail.com"]
        l.extend([li.email for li in us])
        to_list=l
        from_email=settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, l, fail_silently=False)
        crea.save()
        return redirect('allerte')
    context={
        'ut':ut,
        'maladie':maladie,
        'alertes':Alerte.objects.all(),
        'notif':Alerte.objects.filter(Dates__date=auj),
        "domain":current_site.domain,
        
        
    }
    
    return render(request, "add_alerte.html", context)
def modifier(request):
    if request.method == "POST" or request.method == "FILES":
        ids=request.POST.get('id')
        username=request.POST.get('username')
        firstname=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        statut=request.POST.get('statut')
        etat=request.POST.get('etat')
        photo=request.FILES['photo'] or None
        Lieu=request.POST.get('lieu')
        
        
        #if username.isalnum():
         #   messages.error(request,"le nom doit etre alphanumérique")
        #    return redirect('registe')
        
        createutili=User.objects.get(id=ids)
        createutili.username=username
        createutili.first_name=firstname
        createutili.last_name=last_name
        createutili.Photo=photo
        createutili.Lieu=Lieu
        createutili.statut=statut
        createutili.Etat_civil=etat
        createutili.Dates=createutili.Dates
        createutili.email=email
        createutili.save()
        
        return redirect('accueil')
        
            
    
    return render(request, "compte.html")



@login_required
def alertes(request):
    ut=request.user
    allerts=Alerte.objects.all().order_by('Dates')
    context={
        'ut':ut,
        'allertes':allerts,
        'notif':Alerte.objects.filter(Dates__date=auj),
        
    }
    return render(request, "listes_allertes.html", context)

@login_required
def mod_alerte(request):
    return render(request, "mod_alerte.html")

@login_required
def supp(request, id):
    ids=User.objects.get(id=id)
    ids.delete()
    return redirect("list_agents")


@login_required
def list_agents(request):
    notif=Alerte.objects.filter(Dates=auj)
    agents=User.objects.all()
    if request.method=="GET":
        ag=request.GET.get('agents')
        if ag is not None:
            agents=User.objects.filter(Nom__icontains=ag)
    ut=request.user
    
    context={
        'ut':ut,
        'agents':agents,
        'notif':Alerte.objects.filter(Dates__date=auj),
        
    }
    return render(request, "listes_agents.html", context)

@login_required
def profil_agents(request, id):
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
    return render(request, "profiles.html", context)
@login_required
def list_maladies(request):
    ut=request.user
    
    mal=Maladie.objects.all()
    
    context={
        'mal':mal,
        'ut':request.user,
        'notif':Alerte.objects.filter(Dates__date=auj),
        
    }
    return render(request, "listes_maladie.html", context)




@login_required
def compte(request, id):
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
    return render(request, "compte.html", context)


def registe(request):
    org=Organisation.objects.all()
    if request.method == "POST":
        nom=request.POST.get('username')
        firstname=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        civil=request.POST.get('civil')
        password2=password1
        photo=request.FILES['photo'] or None
        Lieu=request.POST.get('lieu')
        orgs="STAND_UP"
        statut=request.POST.get('statut')
        tel=request.POST.get('tel')
        
        
        username=nom
        if User.objects.filter(username=username):
            messages.error(request,"ce nom d'utilisateur existe dèja")
            return redirect('register')
        #if User.objects.filter(email=email):
           # messages.error(request, "cette addresse mail existe dèja, veuillez entré une nouvelle addresse")
           # return redirect('registe')
        #if username.isalnum():
         #   messages.error(request,"le nom doit etre alphanumérique")
        #    return redirect('registe')
        if password1 != password2:
            messages.error(request, "les deux mots de passes sont différents")
            return redirect('register')
        createutili=User.objects.create_user(username, email, password1)
        #generation matricule
        
        createutili.first_name=firstname
        createutili.last_name=last_name
        createutili.Photo=photo
        createutili.Lieu=Lieu
        createutili.Organisation=orgs
        createutili.statut=statut
        createutili.Matricule="ADMIN"
        createutili.Etat_civil=civil
        createutili.Nom=nom
        createutili.Tel=tel
        
      
        createutili.save()
       
        
        
        
        return redirect('logina')
        
    context={
            'org':org
        }    
    return render(request, "register.html", context)

def add_agents(request):
    current_site = get_current_site(request) 
    site_url = f"https://{current_site.domain}"
    org=Organisation.objects.all()
    if request.method == "POST":
        nom=request.POST.get('username')
        firstname=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password1=f"1234{nom[0]}{firstname[0]}{last_name[0]}{auj.year}"
        password2=password1
        photo=request.FILES['photo'] or None
        Lieu=request.POST.get('lieu')
        orgs=request.POST.get('org')
        statut=request.POST.get('statut')
        f1=nom[0]
        f2=firstname[0]
        f3=last_name[0]
        anne=auj.year
        mat=f"SENET{anne}{f1}{f2}{f3}-{statut}"
        username=mat
        if User.objects.filter(username=username):
            messages.error(request,"ce nom d'utilisateur existe dèja")
            return redirect('addagents')
        if User.objects.filter(email=email):
            pass
        #if username.isalnum():
         #   messages.error(request,"le nom doit etre alphanumérique")
        #    return redirect('registe')
        if password1 != password2:
            messages.error("les deux mots de passes sont différents")
            return redirect('addagents')
        createutili=User.objects.create_user(username, email, password1)
        #generation matricule
        try:
            createutili.first_name=firstname
            createutili.last_name=last_name
            createutili.Photo=photo
            createutili.Lieu=Lieu
            createutili.Organisation=orgs
            createutili.statut=statut
            createutili.Matricule=mat
            createutili.Stand_up=False
            createutili.Nom=nom
            createutili.Tel=tel
            
            subject="OBTENTION MATRICULE STAND_UP"
            message=f""" Bonjour cher (chère) partenaire,\n
                    Pour accéder à la plateforme de suivi des alertes STANDUP, voici vos coordonnées :\n
                    -	Code Utilisateur :{mat}
                    -	Mot de passe :{password1}
                    Notez ces informations en lieu sûr pour votre usage futur, et ne les divulguez à personne.\n

                    Vous recevez cet email parce que vous travaillez pour une organisation qui participe au projet SENET avec STAND-UP. \n Ce projet vise à implémenter la surveillance épidémiologique par notification électronique en temps réel au Nord Kivu. 
                    Si vous ignorer tout sur ce projet, prière ignorer cette notification et accepter toutes nos excuses. 
                    Sinon, veuillez cliquer sur le lien: {site_url} suivant pour vous connecter à la plateforme :
                    """
            
            from_email=settings.EMAIL_HOST_USER
            l=[email]
            
            to_list=l
            send_mail(subject, message, from_email, to_list, fail_silently=False)
            createutili.save()
        
            
            
            
            return redirect('addagents')
        except:
            render(request, "error_4002.html")
        
    context={
            'org':org,
            'ut':request.user,
            'notif':Alerte.objects.filter(Dates__date=auj),
        }    
    return render(request, "add_agents.html", context)




@login_required
def deconnexion(request):
    logout(request)
    return redirect('logine')

def logina(request):
    if request.method=="POST":
        usernames=request.POST.get('username')
        password=request.POST.get('password') 
        user=authenticate(request, username=usernames, password=password)
        try:
            my_user= User.objects.get(username=usernames)
            if user is not None and user.is_active:
                login(request, user)
                if my_user.Stand_up:
                    messages.success(request, "bienvenue1")
                    return redirect('accueil')
                else:
                    messages.success(request, "bienvenue")
                    return redirect('indexs')
                
            elif my_user.is_active == False:
                messages.error(request, "vous n'avez pas confimez l'addresse")
            else:
                messages.error(request, "Numéro matricule ou mot de passe incorrect")
                return redirect('logina')
        except:
            return redirect('logina')
        
    return render(request, "login.html", )


def loginse(request):
    if request.method=="POST":
        usernames=request.POST.get('username')
        password=request.POST.get('password') 
        user=authenticate(request, username=usernames, password=password)
        try:
            my_user= User.objects.get(username=usernames)
            if user is not None and user.is_active:
                login(request, user)
                if my_user.Stand_up:
                    messages.success(request, "bienvenue1")
                    return redirect('accueil')
                else:
                    messages.success(request, "bienvenue")
                    return redirect('accueil1')
                
            elif my_user.is_active == False:
                messages.error(request, "vous n'avez pas confimez l'addresse")
            else:
                messages.error(request, "Numéro matricule ou mot de passe incorrect")
                return redirect('logine')
        except:
            messages.error(request, "vous venez de saisir les données invalides")
            return redirect('logine')
        
    return render(request, "login1.html", )