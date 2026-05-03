from django import forms
from .models import Einkauf, Laden


class EinkaufForm(forms.ModelForm):
    class Meta:
        model = Einkauf
        fields = ['artikel', 'laden']
        widgets = {
            'artikel': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Artikel eingeben...',
                'autocomplete': 'off',
            }),
            'laden': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'artikel': 'Artikel',
            'laden': 'Laden',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['laden'].empty_label = 'Egal wo'
        self.fields['laden'].required = False


class EinkaufEditForm(forms.ModelForm):
    class Meta:
        model = Einkauf
        fields = ['artikel', 'laden', 'gekauft']
        widgets = {
            'artikel': forms.TextInput(attrs={'class': 'form-input'}),
            'laden': forms.Select(attrs={'class': 'form-select'}),
            'gekauft': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['laden'].empty_label = 'Egal wo'
        self.fields['laden'].required = False
