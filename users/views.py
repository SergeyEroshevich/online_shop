from django.shortcuts import render, redirect
from users.forms import ChangeUserlnfoForm


def profile(request):
    return render(request, 'account/profile.html')

def change_profile(request):
    user = request.user
    form = ChangeUserlnfoForm(initial={'first_name': user.first_name,
                                       'last_name': user.last_name,
                                       'email': user.email,
                                       'postal_code': user.postal_code,
                                       'city': user.city,
                                       'street': user.street,
                                       'house': user.house,
                                       'building': user.building,
                                       'apartment': user.apartment,
                                       'phone': user.phone}
                              )
    if request.method == 'POST':
        form = ChangeUserlnfoForm(request.POST)
        if form.is_valid():
            postal_code = form.cleaned_data.pop('postal_code')
            city = form.cleaned_data.pop('city')
            street = form.cleaned_data.pop('street')
            house = form.cleaned_data.pop('house')
            building = form.cleaned_data.pop('building')
            apartment = form.cleaned_data.pop('apartment')
            phone = form.cleaned_data.pop('phone')
            user.postal_code = postal_code
            user.city = city
            user.street = street
            user.house = house
            user.building = building
            user.apartment = apartment
            user.phone = phone
            user.first_name = form.cleaned_data.pop('first_name')
            user.last_name = form.cleaned_data.pop('last_name')
            user.email = form.cleaned_data.pop('email')
            user.save()
            return redirect('/profile/')
    context = {'form': form}
    return render(request, 'account/change_profile.html', context)