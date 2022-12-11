from django import forms
from .models import Order

def validator_phone(value):
    if not value.isnumeric():
        raise forms.ValidationError('Поле должно содержать только цифры')
    if len(value) < 9:
        raise forms.ValidationError('Некорректный номер')


class OrderCreateForm(forms.ModelForm):
    phone = forms.CharField( label='Телефон ', validators=[validator_phone], widget=forms.TextInput(attrs={'placeholder': 'телефон'}))
    city = forms.CharField( label='Город', widget=forms.TextInput(attrs={'placeholder': 'город'}))
    street = forms.CharField( label='Улица', widget=forms.TextInput(attrs={'placeholder': 'улица'}))
    house = forms.CharField( label='Дом', widget=forms.TextInput(attrs={'placeholder': 'дом'}))

    class Meta:
        model = Order
        fields = ['phone','payment', 'delivery','postal_code', 'city', 'street', 'house', 'building', 'apartment']

    # def __init__(self, *args, **kwargs):
    #     super(OrderCreateForm, self).__init__(*args, **kwargs)
    #     for field in iter(self.fields):
    #         self.fields[field].widget.attrs.update({'class': 'form-control'})

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['postal_code'].widget.attrs.update({'placeholder': 'почтовый индекс'})
        self.fields['building'].widget.attrs.update({'placeholder': 'корпус'})
        self.fields['apartment'].widget.attrs.update({'placeholder': 'квартира'})