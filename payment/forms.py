

from django.forms import forms, ModelForm

from .models import ShppingAddress



class ShippingForm(ModelForm):

    class Meta:

        model = ShppingAddress

        fields = ['full_name', 'email', 'address1', 'address2', 'city', 'state', 'zipcode']

        exclude = ['user'],