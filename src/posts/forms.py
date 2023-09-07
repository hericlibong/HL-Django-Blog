from django import forms
from froala_editor.widgets import FroalaEditor

from . import models

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['photo', 'caption']
 
class PageForm(forms.ModelForm):
      content = forms.CharField(widget=FroalaEditor) 
      
class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment 
        fields = ['title', 'body']
        
        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control'}),
            'body':forms.Textarea(attrs={'class':'form-control'})
        }
             
 