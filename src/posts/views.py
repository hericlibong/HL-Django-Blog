from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from posts.models import BlogPosts, Comment
from authentication.models import BlogUser
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .forms import PhotoForm, CommentForm 
from . import forms
from django.db.models import Q
from django.templatetags.static import static



# class BlogHome(ListView):
#     model = BlogPosts
#     template_name = 'posts/blog_post.html'
#     context_object_name = 'posts'
    
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         if self.request.user.is_authenticated:
#             return queryset
#         return queryset.filter(published=True)

class BlogHome(ListView):
    model = BlogPosts
    template_name = 'posts/blog_post.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Si l'utilisateur est un superuser, affichez tous les articles
        if user.is_superuser:
            return queryset

       # Si l'utilisateur est authentifié et est un créateur, affichez ses propres articles non publiés
        if user.is_authenticated and user.role == BlogUser.CREATOR:
            return queryset.filter(Q(author=user) | Q(published=True))

        # Si l'utilisateur est authentifié en tant que Suscriber, affichez uniquement les articles publiés
        if user.is_authenticated and user.role == BlogUser.SUSCRIBER:
            return queryset.filter(published=True)

        # Sinon, affichez uniquement les articles publiés
        return queryset.filter(published=True)
    # SUSCRIBER
    
@method_decorator(login_required, name="dispatch") 
@method_decorator(permission_required('posts.add_blogposts', raise_exception=True), name='dispatch')
class BlogPostCreate(CreateView):
    model = BlogPosts
    template_name = 'posts/blogpost_create.html'
    fields = ['title', 'content', 'category', 'thumbnail', 'published',]
    
    def form_valid(self, form):
        # Associez le modèle BlogPosts avec le fichier téléchargé
        form.instance.author = self.request.user
        form.instance.thumbnail = self.request.FILES['thumbnail']
        return super().form_valid(form)
    
    
@method_decorator(login_required, name="dispatch") 
@method_decorator(permission_required('posts.change_blogposts', raise_exception=True), name='dispatch') 
class BlogPostUpdate(UpdateView):
    model = BlogPosts
    template_name = 'posts/blogpost_edit.html'
    fields = ['title', 'content', 'category', 'published', ]
    
    

class BlogPostDetail(DetailView):
    model = BlogPosts
    template_name = 'posts/blogpost_detail.html'    
    context_object_name = "post"
    
    
@method_decorator(login_required, name="dispatch") 
@method_decorator(permission_required('posts.delete_blogposts', raise_exception=True), name='dispatch')  
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


@method_decorator(login_required, name = "dispatch")
class AdCommentPostView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/add_comment.html' 
    success_url = reverse_lazy('home') 
    
    
    def form_valid(self, form):
        post = BlogPosts.objects.get(slug = self.kwargs['slug'])
        form.instance.post = post
        # récupérer l'utilisateur connecté
        author = self.request.user

            
        #récupérer l'image de profil de l'auteur
        author_profile_picture = author.profile_photo
        form.instance.author = author
        form.instance.profile_photo = author_profile_picture
        
    
        #form.instance.author = self.request.user
        return super().form_valid(form)


# @method_decorator(login_required, name="dispatch")
# class AdCommentPostView(CreateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = "posts/add_comment.html"
#     success_url = reverse_lazy("home")

#     def form_valid(self, form):
#         post = BlogPosts.objects.get(slug=self.kwargs["slug"])
#         form.instance.post = post
#         # Récupérer l'utilisateur connecté
#         author = self.request.user

#         if author.profile_photo:
#             # Utilisateur a une photo de profil, utilisez-la
#             form.instance.picture = author.profile_photo
#         else:
#             # Utilisateur n'a pas de photo de profil, utilisez l'icône par défaut
#             form.instance.picture = static("images/icon_sample.png")

#         form.instance.author = author
#         return super().form_valid(form)

    
  
    
    
    
    
    
    