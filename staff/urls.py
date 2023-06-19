from django.urls import path
from .views import (StaffView,
                    ProductCreateView,
                    ProductListView,
                    ProductUpdateView,
                    ProductDeleteView,
                    CouponCreateView,
                    CouponListView,
                    CouponUpdateView,
                    CouponDeleteView,
                    )

app_name = 'staff'

urlpatterns = [
    path('', StaffView.as_view(), name='staff'),
    path('create/', ProductCreateView.as_view(), name='staff-product-create'),
    path('products/', ProductListView.as_view(), name='staff-product-list'),
    path('products/<pk>/update/',
         ProductUpdateView.as_view(), name='staff-product-update'),
    path('products/<pk>/delete/',
         ProductDeleteView.as_view(), name='staff-product-delete'),
    path('coupon-create/', CouponCreateView.as_view(), name='staff-coupon-create'),
    path('coupon-list/', CouponListView.as_view(), name='staff-coupon-list'),
    path('coupon-update/<int:pk>/', CouponUpdateView.as_view(), name='staff-coupon-update'),
    path('coupon-delete/<int:pk>/', CouponDeleteView.as_view(), name='staff-coupon-delete'),
]
