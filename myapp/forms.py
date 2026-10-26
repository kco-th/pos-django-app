from django import forms
from .models import Category,Unit,Product
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
class CategoryForm(forms.ModelForm):
# To specify which model the form works with and which fields should be displayed '''
  class Meta:
    model = Category
    fields = ['name', 'description']
#Unit
class UnitForm(forms.ModelForm):
# To specify which model the form works with and which fields should be displayed '''
  class Meta:
    model = Unit
    fields = ['name', 'description']

#Product form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'unit',
            'price',
            'stock',
            'description',
            'is_active',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter product name'
                }
            ),

            'category': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'unit': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'placeholder': 'Enter price'
                }
            ),

            'stock': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter stock'
                }
            ),

            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter description'
                }
            ),

            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
        }
# Register form

class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = UserProfile
    fields = ('username', 'email', 'role')
    widgets = {
                'username': forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Enter user name'
                    }
                ),
                'email': forms.TextInput(
                        attrs={
                            'class': 'form-control',
                            'placeholder': 'Enter email'
                        }
                    ),
                'role': forms.Select(
                    attrs={
                        'class': 'form-control'
                    }
                ),
    }

