from django import forms

class PaymentForm(forms.Form):
    card_name = forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre en la Tarjeta'}), required=True)
    card_number = forms.CharField(max_length=16, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Tarjeta'}), required=True)
    card_exp_date = forms.CharField(max_length=5, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}), required=True)
    card_cvv_number = forms.CharField(max_length=4, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número CVV'}), required=True)
    card_address1 = forms.CharField(max_length=255, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección de Facturación Línea 1'}), required=True)
    card_address2 = forms.CharField(max_length=255, required=False, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección de Facturación Línea 2'}))
    card_city = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}), required=True)
    card_state = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado/Provincia'}), required=True)
    card_zipcode = forms.CharField(max_length=20, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal'}), required=True)
    card_country = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}), required=True)