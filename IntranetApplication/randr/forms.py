from django import forms
from django.forms import ModelForm

from .models import Recognition, Associate

class RecognitionForm(ModelForm):
        ''' recognition_by = forms.CharField(
            widget=forms.TextInput(attrs={'readonly':'readonly'})
        )'''
	class Meta:
		model = Recognition
		fields = ['associate', 'annotation_title', 'annotation_desc', 'recognition_by']
		
