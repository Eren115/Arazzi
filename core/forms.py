from django import forms

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()

class CheckoutForm(forms.Form):
    email = forms.EmailField(max_length=100)
    full_name = forms.CharField(max_length=100)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    # zip = forms.CharField(max_length=100)
    stripe_token = forms.CharField(max_length=255)