from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.signals import post_save
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
# from .filter import OrderFilter
from django_filters.views import BaseFilterView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .filter import OrderFilter
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from products.models import Rating


class OrdersPageView(TemplateView):
    template_name = 'orders/orders.html'


@login_required()
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = Order(buyer=request.user, **form.cleaned_data)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                product = item['product']
                quantity = item['quantity']
                product.stock -= quantity
                product.save()
            # очистка корзины
            cart.clear()
            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm(initial={'phone': request.user.phone,
                                        'city': request.user.city,
                                        'postal_code': request.user.postal_code,
                                        'street': request.user.street,
                                        'house': request.user.house,
                                        'building': request.user.building,
                                        'apartment': request.user.apartment,
                                        'email': request.user.email
                                        })
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})


@login_required()
def detail_order(request, id):
    order = get_object_or_404(Order, id=id)
    items = OrderItem.objects.filter(order_id=order)
    rating = Rating.objects.filter(user=request.user)
    rating = [x.product for x in rating]
    if request.method == 'POST':
        if request.POST.get('status'):
            order.status = request.POST['status']
            if request.POST['status'] == 'Отменен':
                for item in items:
                    product = item.product
                    product.stock += item.quantity
                    product.save()
        if request.POST.get('paid'):
            order.paid = request.POST['paid']
        order.save()
    context = {'order': order, 'items': items, 'rating': rating}
    return render(request, 'orders/detail_order.html', context)


# все заказы с сайта для персонала
class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, BaseFilterView, ListView):
    model = Order
    paginate_by = 10
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    permission_required = 'users.is.staff'
    filterset_class = OrderFilter


# мои заказы
class MyOrderListView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 5
    template_name = 'orders/my_orders.html'
    context_object_name = 'orders'
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        self.object_list = super(MyOrderListView, self).get_queryset()
        self.object_list = self.object_list.filter(buyer=request.user)
        context = self.get_context_data()
        return self.render_to_response(context)


# детали заказа
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'orders/detail_order.html'
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        items = OrderItem.objects.filter(order_id=self.object)
        rating = Rating.objects.filter(user=request.user)
        rating = [x.product for x in rating]
        context = self.get_context_data(object=self.object)
        context['items'] = items
        context['rating'] = rating
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        items = OrderItem.objects.filter(order_id=order)
        if request.POST.get('status'):
            order.status = request.POST['status']
            if request.POST['status'] == 'Отменен':
                for item in items:
                    product = item.product
                    product.stock += item.quantity
                    product.save()
        if request.POST.get('paid'):
            order.paid = request.POST['paid']
        order.save()
        context = {'order': order, 'items':items}
        return self.render_to_response(context)


@receiver(post_save, sender=Order)
def mail_make_order(sender, **kwargs):
    subject = 'Оформление заказа в магазине'
    html_message = render_to_string('orders/message_order.html', {'order': kwargs.get('instance')})
    plain_message = strip_tags(html_message)
    from_email = 'micromagic.by@yandex.by'
    instance = kwargs.get('instance')
    to_mail = instance.buyer.email
    send_mail(subject, plain_message, from_email, [to_mail], html_message=html_message)






