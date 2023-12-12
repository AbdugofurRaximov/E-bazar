from django.test import TestCase
from users.models import CustomUser
from .models import Category, Products


class ProductTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(username='Admin123', email='admin@gmail.com')
        user.set_password('my_pass')
        user.save()
        self.client.login(username='Admin123', password='my_pass')

    def test_product_created(self):
        Category.objects.create(name='cat')
        response = self.client.post(
            'products/new',
            data={
                'title': 'my_title',
                'description': 'pr desc',
                'price': 123,
                'category': 1,
                'address': 'pr address',
                'phone_number': '+998998712337',
                'tg_username': 'users',
            }
        )
        product = Products.objects.get(id=1)
        self.assertEqual(product.title, 'my title')
        self.assertEqual(product.description, 'pr desc')
        self.assertEqual(product.price, 123)
        self.assertEqual(product.address, 'pr address')
        self.assertEqual(product.category.id, 1)


        second_response=self.client.post(
            'products/1/update',
            data={
                'title': 'my_titles',
                'description': 'pr descr',
                'price': 1234,
                'category': '1',
                'address': 'pr adress',
                'phone_number': '+998997841123',
                'tg_username': 'users',
            }
        )

        product= Products.objects.get(id=1)
        self.assertEqual(product.title, 'my_titles'),
        self.assertNotEqual(product.title, 'my_title'),
        self.assertEqual(product.description, 'pr descr'),
        self.assertEqual(product.price, 1234),
        self.assertEqual(product.address, 'pr adress'),
        self.assertEqual(product.category.id, 1)


        third_response = self.client.post(
            'products/1/delete',
        )
        self.assertEqual(Products.objects.all().count(), 0)

