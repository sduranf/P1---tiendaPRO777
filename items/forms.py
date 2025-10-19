from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    ai_prompt = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Describe the clothing item you want to create',
        required=True,
        help_text='AI will generate a description, image, and estimate the price based on your description'
    )

    class Meta:
        model = Item
        fields = ['title', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }