from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  

from django.contrib.auth.models import User

from django.forms import ModelForm  

from django.forms.widgets import PasswordInput, TextInput





## REGITSER USER FORM
class CreateUserForm(UserCreationForm):

    email = forms.EmailField(required=True) ## mark email field as required

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']
        


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError("This email address is already in use.")
        
        return email




## LOGIN USER FORM
class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())



# UDPATE USER DETAILS FORM

class UpdateUserForm(ModelForm): 
    password = None 

    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email  # Get the current email from the instance

        if not email:  # Check if email is empty
            raise forms.ValidationError("Email address cannot be empty.")

        if email != current_email:  # Check if email has been changed
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email address is already in use.")
        
        return email


