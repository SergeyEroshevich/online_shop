from users.models import CustomUser
from django.db import models
from django.urls import reverse
from products.models import Product


class Order(models.Model):
    CHOICES_PAYMENT = (
        ('Наличные','Наличные при получении'),
        ('Оплата картой', 'Оплата картой'),
    )

    CHOICES_DELIVERY = (
        ('Самовывоз', 'Самовывоз'),
        ('Курьер', 'Курьер'),
        ('Почта', 'Почта'),
    )

    CHOICES_STATUS = (
        ('Принято в обработку', 'Принято в обработку'),
        ('Упакован и отправлен', 'Упакован и отправлен'),
        ('Доставлен покупателю', 'Доставлен покупателю'),
        ('Отменен', 'Отменен'),
    )

    buyer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    status = models.CharField(max_length=50, default='Принято в обработку', choices=CHOICES_STATUS, verbose_name='Статус заказа')
    payment = models.CharField(max_length=50, choices=CHOICES_PAYMENT, verbose_name='Способ оплаты')
    delivery = models.CharField(max_length=50, choices=CHOICES_DELIVERY, verbose_name='Способ доставки')
    phone = models.CharField(max_length=13, verbose_name='Телефон')
    postal_code = models.CharField(max_length=20, verbose_name='почтовый индекс', blank=True)
    city = models.CharField(max_length=100, verbose_name='город')
    street = models.CharField(max_length=100, verbose_name='улица')
    house = models.CharField(max_length=100, verbose_name='дом')
    building = models.CharField(max_length=100, verbose_name='корпус', blank=True)
    apartment = models.CharField(max_length=100, verbose_name='квартира', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name='Оплачено')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_absolute_url(self):
        return reverse('detail_order', args=[self.id])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

