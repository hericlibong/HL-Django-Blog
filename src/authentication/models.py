from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image



class BlogUser(AbstractUser):
    
    CREATOR = 'CREATOR'
    SUSCRIBER = 'SUSCRIBER'
    
    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUSCRIBER, 'Abonné'),
    )
    profile_photo = models.ImageField(blank= True, upload_to='blog', verbose_name='Photo Profile')
    role = models.CharField(max_length=30, choices= ROLE_CHOICES, verbose_name= 'Rôle')
    
    IMAGE_MAX_SIZE = (250, 250)
    
    def resize_profile_photo(self):
        if self.profile_photo:
            image = Image.open(self.profile_photo.path)
            #new_size = (128, 138)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.profile_photo.path)
            
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_profile_photo()
    