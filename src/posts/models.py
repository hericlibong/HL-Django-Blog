from django.urls import reverse
from django.utils.text import slugify
from django.db import models
from authentication.models import BlogUser
from django.conf import settings
from ckeditor.fields import RichTextField
#from froala_editor.fields import FroalaField
from PIL import Image



class Tags(models.Model):
    name = models.CharField(max_length=255, unique=True) 
    
    class Meta :
        verbose_name_plural = "Tags"
    
    def __str__(self):
        return self.name
     
class Photo(models.Model):
    photo = models.ImageField(upload_to="blog")
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    blogposts = models.ForeignKey('BlogPosts', related_name= 'blog_posts', on_delete=models.CASCADE)
    


class BlogPosts(models.Model):
    
    
    CATEGORY_CODE = 'Code'
    CATEGORY_STORIES = 'Stories'
    
    CATEGORIES_CHOICES = [
        (CATEGORY_CODE, 'Code'),
        (CATEGORY_STORIES, 'Stories'),
    ]
    
    title = models.CharField(max_length=255, unique = True, verbose_name= 'Titre')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(BlogUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    created_on = models.DateField(blank=True, null=True)
    published =models.BooleanField(default=False, verbose_name='Publié')
    
    #### Choose an Editor ####
    
    #content = FroalaField()
    content = RichTextField(blank=True, null=True, verbose_name= 'Contenu')
    #content = models.TextField(blank=True, verbose_name='Contenu')
    
    
    category = models.CharField(max_length=50, choices= CATEGORIES_CHOICES)
    tags = models.ManyToManyField(Tags, related_name='tags')
    thumbnail = models.ImageField(blank=True, upload_to='blog')
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, related_name='photos_for_blog_posts')
    
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
    
       
            