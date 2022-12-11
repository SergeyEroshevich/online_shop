from django.db import models
from django import forms
import django_filters

from orders.models import Order


class OrderFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(label='Упорядочить', choices=(('id', 'номер заказа'),))
    paid = django_filters.BooleanFilter()

    class Meta:
        model = Order
        fields = ['paid', 'status', 'payment', 'delivery']

