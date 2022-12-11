from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


def validator_phone(value):
    if not value.isnumeric():
        raise forms.ValidationError('Поле должно содержать только цифры')
    if len(value) < 9:
        raise forms.ValidationError('Некорректный номер')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'

class ChangeUserlnfoForm(forms.ModelForm):
    phone = forms.CharField( label='Телефон', validators=[validator_phone], required=False)
    postal_code = forms.CharField(max_length=20, label='Почтовый индекс', required=False)
    city = forms.CharField(max_length=100, label='Город', required=False)
    street = forms.CharField(max_length=100, label='Улица', required=False)
    house = forms.CharField(max_length=100, label='Дом', required=False)
    building = forms.CharField(max_length=100, label='Корпус', required=False)
    apartment = forms.CharField(max_length=100, label='Квартира', required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'phone', 'postal_code', 'city', 'street', 'house', 'building', 'apartment')