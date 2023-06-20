from django import forms
from django.utils.translation import gettext_lazy as _
from core.models import Item, Coupon
from core.templatetags.custom_filters import add_thousands_separator



class ProductForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'title',
            'image',
            'price',
            'discount_price',
            'on_sale',
            'category',
            'label',
            'slug',
            'description',
        ]
        labels = {
            'title': _('Nombre'),
            'image': _('Imagen'),
            'price': _('Precio'),
            'discount_price': _('Precio con descuento'),
            'on_sale': _('¿En Oferta?'),
            'category': _('Categoría'),
            'label': _('Etiqueta'),
            'slug': _('Slug'),
            'description': _('Descripción'),
        }


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'amount', 'active']
        labels = {
            'code': _('Nombre del Código'),
            'amount': _('Monto de descuento'),
            'active': _('¿Activo?'),
        }



