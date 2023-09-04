from django.urls import reverse
from django.utils.text import slugify
from django.db import models
from authentication.models import BlogUser
from django.conf import settings



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
    content = models.TextField(blank=True, verbose_name='Contenu')
    category = models.CharField(max_length=50, choices= CATEGORIES_CHOICES)
    tags = models.ManyToManyField(Tags, related_name='tags')
    thumbnail = models.ImageField(blank=True, upload_to='blog')
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, related_name='photos_for_blog_posts')
    
    
    
    
    
    class Meta:
        ordering = ['-created_on']
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
        
            