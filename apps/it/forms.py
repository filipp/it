# -*- coding: utf-8 -*-

from django import forms
from django.forms.extras.widgets import SelectDateWidget

from apps.it.models import (Issue, Task, Attachment,
                            User, Asset, TaggedItem)

class SmallTextarea(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(SmallTextarea, self).__init__(attrs={'rows': 5})

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset

class SimpleAssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'kind']

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue

class SimpleIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description']
        widgets = {'description': SmallTextarea}

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        widgets = {
            'description': SmallTextarea,
            'due_date': SelectDateWidget
        }

class SimpleTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description']
        widgets = {
            'description': SmallTextarea,
        }
