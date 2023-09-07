from django.shortcuts import redirect, render
from django.views.generic import View, CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import BlogUser

from authentication import forms



class LoginPageView(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm
    
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context ={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            message = 'vous est connecté'
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides'
        return render(request, self.template_name, context={'form': form, 'message':message})
           


def logout_user(request):
    logout(request)
    return redirect('login')


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, "Vous êtes enregistré. Vous pouvez vous connecter")
            
            return redirect('success')
    return render(request, 'authentication/signup.html', context = {'form':form}) 
  
  
def sucess_connexion(request):
    message = 'Félicitations vous êtes enregistré'
    template_name = 'authentication/success.html'
    user = request.user
    return render(request,template_name, context = {'message':message, 'user':user})




def upload_profile_photo(request):
    form = forms.UploadProfilePhotoForm(instance=request.user)
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'authentication/upload_profile_photo.html', context={'form': form})

    


              
