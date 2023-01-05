# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 15:26:04 2022

@author: user
"""

from django import forms
from .models import Photo

class UploadModelForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("image",)
        widgets = {
            "image":forms.FileInput(attrs={"class":"form-control-file"})
            }