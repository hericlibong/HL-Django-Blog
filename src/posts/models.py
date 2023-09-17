from django.urls import reverse
from django.utils.text import slugify
from django.db import models
from authentication.models import BlogUser
from django.conf import settings
#from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
#from froala_editor.fields import FroalaField

from PIL import Image



class Tags(models.Model):
    name = models.CharField(max_length=255, unique=True) 
    
    class Meta :
        verbose_name_plural = "Tags"
    
    def __str__(self):
        return self.name
     

    


class BlogPosts(models.Model):
    
    
    CATEGORY_CODE = 'Code'
    CATEGORY_STORIES = 'Stories'
    
    CATEGORIES_CHOICES = [
        (CATEGORY_CODE, 'Code'),
        (CATEGORY_STORIES, 'Stories'),
    ]
    
    title = models.CharField(max_length=255, unique = True, verbose_name= 'Titre')
    description = models.TextField(blank=True,null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(BlogUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    created_on = models.DateField(blank=True, null=True)
    published =models.BooleanField(default=False, verbose_name='Publié')
    
    #### Choose an Editor ####
    
    #content = FroalaField()
    #content = RichTextField(blank=True, null=True, verbose_name= 'Contenu')
    content = RichTextUploadingField(blank=True, null=True)
    #content = models.TextField(blank=True, verbose_name='Contenu')
    
    
    
    category = models.CharField(max_length=50, choices= CATEGORIES_CHOICES)
    tags = models.ManyToManyField(Tags, related_name='tags')
    thumbnail = models.ImageField(blank=True, upload_to='blog')
  
    
    IMAGE_MAX_SIZE = (646, 347.85)
    
    def resize_thumb(self):
        if self.thumbnail:
            image = Image.open(self.thumbnail)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.thumbnail.path)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_thumb()
        
    class Meta:
        ordering = ['-last_updated']
        verbose_name = "Article"
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def add_tag(self, tag_name):
        tag, _ = Tags.objects.get_or_create(name=tag_name)
        self.tags.add(tag)
        self.save() 
        
    def get_absolute_url(self):
        return reverse('home') 
    
    def get_category_url(self):
        return reverse('category_view', args=[self.category])
    
    #### affichage par catégories #####
    
    # méthode qui renvoie une liste des catégories uniques disponibles
    @classmethod
    def get_available_categories(cls):
        return cls.objects.order_by('category').values_list('category', flat=True).distinct()
    
    # ajoutez une méthode pour obtenir l'URL de filtre pour chaque catégorie.
    @staticmethod
    def get_category_filter_url(category):
        return reverse('home') + f'?category={category}'
    
class Comment(models.Model):
    post = models.ForeignKey(BlogPosts, on_delete=models.CASCADE, related_name = 'comments')
    title = models.CharField(max_length=250, blank=True, null=True, verbose_name="Titre de l'article")
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    picture = models.ForeignKey(BlogUser, on_delete=models.CASCADE, related_name='picture_comment', blank=True, null=True)
    
    def get_author_profile_photo(self):
        return self.author.profile_photo
    
    
    def __str__(self):
        return f'{self.author.username} - {self.title} - {self.created_at}'  
    
    class Meta:
        ordering = ['-created_at']
        
    
    
       
            