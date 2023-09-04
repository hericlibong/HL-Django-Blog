from django.contrib.auth.models import AbstractUser
from django.db import models



class BlogUser(AbstractUser):
    
    CREATOR = 'CREATOR'
    SUSCRIBER = 'SUSCRIBER'
    
    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUSCRIBER, 'Abonné'),
    )
    profile_photo = models.ImageField(blank= True, upload_to='blog', verbose_name='Photo Profile')
    role = models.CharField(max_length=30, choices= ROLE_CHOICES, verbose_name= 'Rôle' )
    