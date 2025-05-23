from django import forms

from .models import ShippingAddress

class ShippingForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = [
            'full_name',
            'phone_number',
            'email',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'postal_code',
        ]
        exclude = ['user',]