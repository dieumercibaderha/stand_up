from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    Photo=models.ImageField(upload_to="Images/", blank=True)
    statut=models.CharField(default="ENQUETEUR", max_length=100)
    Organisation=models.CharField(default="-",max_length=500)
    Lieu=models.CharField(default="-",max_length=200)
    Nom=models.CharField(default="-", max_length=20)
    Dates=models.DateTimeField(auto_now=True)
    Etat_civil=models.CharField(default="Célibataire", max_length=100)
    Stand_up=models.BooleanField(default="True")
    Matricule=models.CharField(default="---", max_length=50)
    
class Maladie(models.Model):
    Nom=models.CharField(max_length=500)
    def __str__(self):
        return self.Nom

class Alerte(models.Model):
    Enqueteur=models.CharField(max_length=500)
    Photo=models.ImageField(upload_to="Images/", blank=True)
    Maladie=models.ForeignKey(Maladie, on_delete=models.CASCADE)
    Cas= models.DecimalField(max_digits=10, decimal_places=0)
    ASC=models.CharField(default="Village", max_length=200)
    Province=models.CharField(default="NORD-KIVU", max_length=200)
    
    Zone_de_sant=models.CharField(max_length=300)
    Dates=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.Enqueteur}/{self.Maladie}/{self.Cas}"
    
    
class Organisation(models.Model):
    Nom=models.CharField(max_length=500)
    Adresse=models.CharField(max_length=500)
    Tel=models.CharField(max_length=200)
    
    def __str__(self):
        return self.Nom