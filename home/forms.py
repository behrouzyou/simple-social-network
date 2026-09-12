from .models import Post,Comment
from django import forms

class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =('body',)
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('body',)
        widgets={
            'body':forms.Textarea(attrs={'class':'form-control','placeholder':'type here'})
        }
class CommentReplyForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('body',)
        widgets={
            'body':forms.Textarea(attrs={'class':'form-control','placeholder':'type here'})
        }

class PostSearchForm(forms.Form):
    search=forms.CharField()