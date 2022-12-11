from django import forms

from .models import Product, Category

class DiscountDeleteForm(forms.Form):
    product_discount = forms.ModelMultipleChoiceField(queryset=Product.objects.filter(discount=True),
                                                      widget=forms.CheckboxSelectMultiple,
                                                      label='Убрать скидку с товара',
                                                      required=False)

class DiscountForm(forms.Form):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              widget=forms.CheckboxSelectMultiple,
                                              label='Выбрать всю категорию для скидки',
                                              required=False)

    product = forms.ModelMultipleChoiceField(queryset=Product.objects.filter(discount=False),
                                             label='Выбрать конкретный товар для скидки',
                                             required=False)

    discount = forms.IntegerField(min_value=0, max_value=100, label='Размер скидки')