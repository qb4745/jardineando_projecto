from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import reverse
from django.views import generic
from core.models import Order, Item, Coupon
from .forms import ProductForm, CouponForm
from .mixins import StaffUserMixin


class StaffView(LoginRequiredMixin, StaffUserMixin, generic.ListView):
    template_name = 'staff/staff.html'
    queryset = Order.objects.filter(ordered=True).order_by('-ordered_date')
    paginate_by = 20
    context_object_name = 'orders'


class ProductListView(LoginRequiredMixin, StaffUserMixin, generic.ListView):
    template_name = 'staff/product_list.html'
    model = Item
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-id')  # Replace 'id' with the appropriate field for ordering




class CouponListView(LoginRequiredMixin, StaffUserMixin, generic.ListView):
    template_name = 'staff/coupon_list.html'
    model = Coupon
    context_object_name = 'coupons'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-id')  # Replace 'id' with the appropriate field for ordering




class ProductCreateView(LoginRequiredMixin, StaffUserMixin, generic.CreateView):
    template_name = 'staff/product_create.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse("staff:staff-product-list")

    def form_valid(self, form):
        form.save()
        return super(ProductCreateView, self).form_valid(form)


class CouponCreateView(LoginRequiredMixin, StaffUserMixin, generic.CreateView):
    template_name = 'staff/coupon_create.html'
    form_class = CouponForm

    def get_success_url(self):
        return reverse("staff:staff-coupon-list")

    def form_valid(self, form):
        form.save()
        return super(CouponCreateView, self).form_valid(form)


class ProductUpdateView(LoginRequiredMixin, StaffUserMixin, generic.UpdateView):
    template_name = 'staff/product_update.html'
    form_class = ProductForm
    queryset = Item.objects.all()

    def get_success_url(self):
        return reverse("staff:staff-product-list")

    def form_valid(self, form):
        form.save()
        return super(ProductUpdateView, self).form_valid(form)


class CouponUpdateView(LoginRequiredMixin, StaffUserMixin, generic.UpdateView):
    template_name = 'staff/coupon_update.html'
    form_class = CouponForm
    queryset = Coupon.objects.all()

    def get_success_url(self):
        return reverse("staff:staff-coupon-list")

    def form_valid(self, form):
        form.save()
        return super(CouponUpdateView, self).form_valid(form)


class ProductDeleteView(LoginRequiredMixin, StaffUserMixin, generic.DeleteView):
    template_name = 'staff/product_delete.html'
    queryset = Item.objects.all()

    def get_success_url(self):
        return reverse("staff:staff-product-list")


class CouponDeleteView(LoginRequiredMixin, StaffUserMixin, generic.DeleteView):
    template_name = 'staff/coupon_delete.html'
    queryset = Coupon.objects.all()

    def get_success_url(self):
        return reverse("staff:staff-coupon-list")


