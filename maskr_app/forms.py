from django import forms
from .models import Images

class ImgForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('image',)
        exclude = ('name',)