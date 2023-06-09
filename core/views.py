from django.shortcuts import render
from django.views.generic import View, ListView, TemplateView, DetailView

from .models import Item

# Create your views here.
class HomeView(TemplateView):
    template_name = "core/home.html"


class ProductsView(ListView):
    model = Item
    paginate_by = 10
    template_name = "core/products.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "core/product.html"