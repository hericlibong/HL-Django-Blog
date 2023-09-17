from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from posts.models import BlogPosts, Comment
from authentication.models import BlogUser
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .forms import CommentForm 
from . import forms
from django.db.models import Q
from django.templatetags.static import static
from django.http import Http404




class BlogHome(ListView):
    model = BlogPosts
    template_name = 'posts/blog_post.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
       
        if user.is_superuser:
            return queryset
        if user.is_authenticated:
            if user.role == BlogUser.CREATOR:
                return queryset.filter(Q(author=user) | Q(published=True))
            if user.role == BlogUser.SUSCRIBER:
                return queryset.filter(published=True)
        
        return queryset.filter(published=True)

    
    

    
@method_decorator(login_required, name="dispatch") 
@method_decorator(permission_required('posts.add_blogposts', raise_exception=True), name='dispatch')
class BlogPostCreate(CreateView):
    model = BlogPosts
    template_name = 'posts/blogpost_create.html'
    fields = ['title', 'description', 'category', 'thumbnail', 'content', 'published']
    
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
    fields = ['title', 'description', 'content', 'category', 'published', ]
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        # Vérifiez si l'utilisateur connecté est l'auteur de l'article.
        if obj.author != request.user:
            raise Http404("Vous n'êtes pas autorisé à éditer cet article.")
        
        return super().dispatch(request, *args, **kwargs)
    
    

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
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        # Vérifiez si l'utilisateur connecté est l'auteur de l'article.
        if obj.author != request.user:
            raise Http404("Vous n'êtes pas autorisé à supprimer cet article.")
        
        return super().dispatch(request, *args, **kwargs)
    



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
    
    
    ## others views
    
class BlogPostByCategory(ListView):
        model = BlogPosts
        template_name = 'posts/posts_category.html'
        context_object_name = 'post_by_category'
        sucess_url = reverse_lazy('blog')
        
        
        def get_queryset(self):
            """
        Récupère les articles en fonction de la catégorie sélectionnée, ou tous les articles si aucune catégorie n'est spécifiée.
            """
            selected_category = self.request.GET.get('category')
            user = self.request.user
            
            if selected_category:
                queryset= BlogPosts.objects.filter(category=selected_category)
            else:
                queryset = BlogPosts.objects.all()
            
            if user.is_superuser:
                return queryset
            
            if user.is_authenticated:
                if user.role == BlogUser.CREATOR:
                    return queryset.filter(Q(author=user) | Q(published=True))

            if user.role == BlogUser.SUSCRIBER:
                return queryset.filter(published=True)

            return queryset.filter(published=True)
                  
        
        
        def get_context_data(self, **kwargs):
            """
        Ajoute des données de contexte supplémentaires à afficher dans le modèle.
        """
            context = super().get_context_data(**kwargs)
            selected_category = self.request.GET.get('category')
            
            # Compte du nombre d'articles par catégorie
            if selected_category:
                post_by_category = BlogPosts.objects.filter(category=selected_category)
                context['category_post_count'] = post_by_category.count()
            
            # Liste des catégories disponibles
            available_categories = BlogPosts.objects.order_by('category').values_list('category', flat=True).distinct()
            context['available_categories'] = available_categories
            
            return context


#

    
  
    
    
    
    
    
    