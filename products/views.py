from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import InvalidPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django_filters.views import BaseFilterView
from .filter import ProductFilter
from .forms import DiscountForm, DiscountDeleteForm
from .models import Product, Category, Rating
from django.db.models import ExpressionWrapper, F, IntegerField

class ProductListView(BaseFilterView, ListView):
    model = Product
    paginate_by = 5
    template_name = 'products/product_list.html'
    context_object_name = 'product_list'
    filterset_class = ProductFilter
    queryset =  Product.objects.annotate(value_sale=ExpressionWrapper(100 - F('sale') * 100, IntegerField()),
                                        sale_price=F('price') * F('sale')).filter(available=True)

    def get(self, request,  *args, category_slug=None, **kwargs):
        if 'page' in request.GET:
            page_number = request.GET['page']
        else:
            page_number = 1

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            self.object_list = self.get_queryset().filter(category=category)
        else:
            self.object_list = self.get_queryset()
        filter_object_list = ProductFilter(request.GET, queryset=self.object_list)
        self.object_list = filter_object_list.qs
        # self.object_list = self.paginate_queryset(self.object_list, page_number)[2]
        print(self.object_list)
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                from pkg_resources import _
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

    def paginate_queryset(self, queryset, page_size):
        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_('Page is not “last”, nor can it be converted to an int.'))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            from pkg_resources import _
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['filter'] = ProductFilter
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_detail.html'


class RatingDetailView(DetailView):
    model = Product
    context_object_name = 'rating'
    template_name = 'products/review.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # сделано для того чтобы кнопка "Оставить отзыв" показывалась только тем пользователям кто еще не оставлял его:
        users = [x.user for x in self.object.product_rating.all()]
        context = self.get_context_data(object=self.object)
        context['users'] = users
        return self.render_to_response(context)


class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'products/search_results.html'
    queryset = Product.objects.annotate(value_sale=ExpressionWrapper(100 - F('sale') * 100, IntegerField()),
                                        sale_price=F('price') * F('sale')).filter(available=True)

    def get_queryset(self):
        queryset = super(SearchResultsListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query == '':
            pass
        else:
            return queryset.filter(Q(name__icontains=query))


class AddRatinglView(DetailView):
    model = Product
    context_object_name = 'add_rating'
    template_name = 'products/add_review.html'


@login_required()
def add_review(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        rating = Rating.objects.create(product=product, user=request.user, rating=request.POST['simple-rating'], review=request.POST.get('review'))
        rating.save()
        if product.rating == None:
            product.rating = request.POST['simple-rating']
        else:
            count = product.product_rating.count()
            sum = 0
            for i in product.product_rating.all():
                sum += i.rating
            rating = sum/count
            product.rating = round(rating, 1)
        product.save()
        url = f'/products/{pk}/review/'
        return redirect(url)
    context = {'product':product}
    return render(request, 'products/add_review.html', context)


@staff_member_required
def discount_management(request):
    form = DiscountForm()
    form_delete = DiscountDeleteForm()
    products = Product.objects.filter(discount=True)
    if request.method == 'POST':
        if request.POST.get('product'):
            products_for_discount = request.POST.getlist('product')
            for product in products_for_discount:
                product = Product.objects.get(id=product)
                product.discount = True
                sale = 1 - int(request.POST.get('discount'))/100
                product.sale = sale
                product.save()
        if request.POST.get('category'):
            category_discount = request.POST.getlist('category')
            for category in category_discount:
                category = Category.objects.get(id=category)
                products = Product.objects.filter(category=category)
                for product in products:
                    product.discount = True
                    sale = 1 - int(request.POST.get('discount')) / 100
                    product.sale = sale
                    product.save()
        if request.POST.get('product_discount'):
            product_discount = request.POST.getlist('product_discount')
            for product in product_discount:
                product = Product.objects.get(id=product)
                product.discount = False
                product.sale = 1
                product.save()
    context = {'products':products, 'form': form, 'form_delete':form_delete}
    return render(request, 'products/discount_management/discount_management.html', context)