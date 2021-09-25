from django import forms
from django.forms.fields import Field
from .models import Review, Comment

class ReviewForm(forms.ModelForm):

   class Meta:
       model = Review
       fields = ['title', 'content'] 


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields =['text']