import django_filters
from django.forms import TextInput, CheckboxSelectMultiple, CheckboxInput
from .models import Product

class ProductFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='icontains', label='Найти', widget=TextInput(attrs={'placeholder': 'введите название товара'}))
    discount = django_filters.BooleanFilter(method='filter_discount', widget=CheckboxInput)
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt', label='Цена от')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt', label='Цена до')
    ordering = django_filters.OrderingFilter(label='Упорядочить',lookup_expr='in', choices=(('price', 'цена по возрастанию'),
                                                                              ('-price', 'цена по убыванию'),
                                                                              ('name', 'по названию'),
                                                                              ('-rating', 'по рейтингу'),
                                                                              ('-created', 'новые'),))

    def filter_discount(self, queryset, name, value):
        if value == False:
            lookup = '__'.join([name, 'isnull'])
            return queryset.filter(**{lookup: False})
        else:
            return queryset.filter(**{name: value})

    class Meta:
        model = Product
        fields = ['discount', 'ordering']