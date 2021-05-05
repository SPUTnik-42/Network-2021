

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .models import  Post, UserProfile


class CreatePostForm(forms.ModelForm):

    content = forms.CharField(label="Description", widget=forms.Textarea(attrs={
                                    'placeholder': _("What are you thinking about?"),
                                    'autofocus': 'autofocus',
                                    'rows': '3',
                                    'class': 'form-control',
                                    'aria-label': _("post content")
                             }))

    class Meta:
        model = Post
        fields = ["content"]


