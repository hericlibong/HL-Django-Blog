from django import forms
#from froala_editor.widgets import FroalaEditor
from ckeditor.widgets import CKEditorWidget

from . import models


      
class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment 
        fields = ['title', 'body']
        
        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control'}),
            'body':forms.Textarea(attrs={'class':'form-control'})
        }
    body = forms.CharField(widget = CKEditorWidget()) 
             
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = models.BlogPosts
        fields = ['content']

    content = forms.CharField(widget=CKEditorWidget())  