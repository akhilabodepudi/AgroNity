from django import forms

from .models import Crop


class CropForm(forms.ModelForm):
    """Front-end form for farmers to list a crop on the market.

    Uses ``image_url`` (a link to a photo) rather than a file upload, because
    Vercel's serverless filesystem is read-only, so uploaded files can't be
    saved there. To support real uploads, enable Cloudinary (see settings.py).
    """

    class Meta:
        model = Crop
        fields = ['name', 'description', 'quantity', 'price', 'quality', 'health_status', 'image_url']
        labels = {
            'image_url': 'Image URL',
            'health_status': 'Health status',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Alphonso Mango'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description of the crop'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
            'quality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Fresh and Organic'}),
            'health_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Good'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://... link to a crop photo'}),
        }
