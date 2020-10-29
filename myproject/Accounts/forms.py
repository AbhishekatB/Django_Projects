from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import Customer,Nursery_Manager,User,Plants,Images


class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.phone_number=self.cleaned_data.get('phone_number')
        customer.location=self.cleaned_data.get('location')
        customer.save()
        return user

class Nursery_manager_SignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    designation = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_manager = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        manager = Nursery_Manager.objects.create(user=user)
        manager.phone_number=self.cleaned_data.get('phone_number')
        manager.designation=self.cleaned_data.get('designation')
        manager.save()
        return user


class PlantForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput(),initial='user')
    price = forms.CharField()
    class Meta:
        model = Plants
        fields = ('price' ,)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Images
        fields = ('image', )