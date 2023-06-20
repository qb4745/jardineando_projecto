import re
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Donacion


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Cupón de descuento',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)




class DonacionForm(forms.ModelForm):
    telefono = forms.IntegerField(
        error_messages={
            'max_value': 'Ingrese un número de teléfono válido de 9 dígitos.',
        },
        validators=[
            MinValueValidator(100000000, message='Ingrese un número de teléfono válido de 9 dígitos.'),
            MaxValueValidator(999999999, message='Ingrese un número de teléfono válido de 9 dígitos.'),
        ]
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Retrieve the request object
        super().__init__(*args, **kwargs)
        self.fields['codigo_pais'].disabled = True
        self.fields['codigo_pais'].initial = '+56'

    def save(self, commit=True):
        instance = super().save(commit)
        if self.request:
            messages.success(self.request, 'Los datos se han enviado correctamente, pronto nos contactaremos con usted.')
        return instance

    class Meta:
        model = Donacion
        fields = [
            'nombre',
            'apellido',
            'correo',
            'monto',
            'codigo_pais',
            'telefono',
            'rut',
        ]
        labels = {
            'nombre': _('Nombre'),
            'apellido': _('Apellido'),
            'correo': _('Correo electrónico'),
            'monto': _('Monto'),
            'codigo_pais': _('Código de País'),
            'telefono': _('Teléfono'),
            'rut': _('R.U.T.'),
        }




