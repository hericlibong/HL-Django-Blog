from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from posts.models import BlogPosts
from authentication.models import BlogUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
#from .forms import PhotoForm
from . import forms


def is_creator(user):
    try:
        return user.blogUser.role == BlogUser.CREATOR
    except: BlogUser.DoesNotExist
    return False
class BlogHome(ListView):
    model = BlogPosts
    template_name = 'posts/blog_post.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(published=True)
    
@method_decorator(login_required, name = "dispatch")
class BlogPostCreate(CreateView):
    model = BlogPosts
    template_name = 'posts/blogpost_create.html'
    fields = ['title', 'content', 'category', 'thumbnail',]
    
    def form_valid(self, form):
        # Associez le modèle BlogPosts avec le fichier téléchargé
        form.instance.author = self.request.user
        form.instance.thumbnail = self.request.FILES['thumbnail']
        return super().form_valid(form)
    
    
 
class BlogPostUpdate(UpdateView):
    model = BlogPosts
    template_name = 'posts/blogpost_edit.html'
    fields = ['title', 'content', 'category', 'published', ]
    
   
class BlogPostDetail(DetailView):
    model = BlogPosts
    template_name = 'posts/blogpost_detail.html'
    context_object_name = "post"
    
    
@method_decorator(login_required, name="dispatch")   
class BlogPostDelete(DeleteView):
    model = BlogPosts
    template_name = 'posts/blogpost_confirm_delete.html'
    success_url = reverse_lazy("home")
    context_object_name = "post"
    
    
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.username
            photo.save()
            return redirect('home')
    return render(request, 'posts/photo_upload.html', context={'form':form})


    
    
    
    
    
    