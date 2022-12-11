from django.test import Client, TestCase
from django.urls import reverse
from .models import Product

class ProductTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Harry Potter',
            category='JK Rowling',
            price='25.00',
        )

    def test_book_listing(self):
        self.assertEqual(f'{self.product.name}', 'Harry Potter')
        self.assertEqual(f'{self.product.category}', 'JK Rowling')
        self.assertEqual(f'{self.product.price}', '25.00')

    def test_book_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'products/product_list.html')

    def test_book_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        no_response = self.client.get('/products/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'products/product_detail.html')

