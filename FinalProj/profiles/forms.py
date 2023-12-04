from django import forms
from .models import Profile
from catalog.models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'year_created', 'company', 'category', 'image']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'email', 'first_name', 'last_name', 'phone_number']
