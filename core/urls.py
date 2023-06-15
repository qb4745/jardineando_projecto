from django.urls import path
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    ProductsView,
    AddCouponView,
    RequestRefundView
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='core-home'),
    path('checkout/', CheckoutView.as_view(), name='core-checkout'),
    path("products/",ProductsView.as_view(), name="core-products"),
    path('product/<slug>/', ItemDetailView.as_view(), name='core-product'),
    path('order-summary/', OrderSummaryView.as_view(), name='core-order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='core-add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='core-add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='core-remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='core-remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='core-payment'),
    path('request-refund/', RequestRefundView.as_view(), name='core-request-refund')
]