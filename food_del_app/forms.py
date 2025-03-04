from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Menus, Restaurants,Foodie

class MenuForm(forms.ModelForm):
    restaurant_id = forms.ModelChoiceField(queryset=Restaurants.objects.all(), label="Restaurant")

    class Meta:
        model = Menus
        fields = ['restaurant_id', 'name', 'description', 'price', 'image_url']


class FoodieSignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Foodie
        fields = ['first_name', 'last_name', 'address1', 'phone_no1', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'address1': 'Address',
            'phone_no1': 'Phone Number',
            'email': 'Email',
            'password': 'Password',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class FoodieLoginForm(AuthenticationForm):
    username = forms.CharField(label="fname", max_length=50)
    
    
    

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}))


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurants
        fields = ['name', 'address', 'phone_no','image_url']  # Include the fields you want to update

class DishForm(forms.ModelForm):
    class Meta:
        model = Menus
        fields = ['name','description', 'price','image_url']  # Include the fields you want to update