from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Book, Transaction

class CheckoutReturnTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.book = Book.objects.create(title='T1', author='A', isbn='111', copies_available=1)
        self.client = APIClient()
        self.client.login(username='testuser', password='pass')

    def test_checkout_decrements_copies(self):
        resp = self.client.post('/api/transactions/checkout/', {'book_id': self.book.id}, format='json')
        self.assertEqual(resp.status_code, 201)
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_available, 0)
        self.assertTrue(Transaction.objects.filter(user=self.user, book=self.book, transaction_type='checkout').exists())

    def test_cannot_checkout_when_no_copies(self):
        self.client.post('/api/transactions/checkout/', {'book_id': self.book.id}, format='json')
        resp = self.client.post('/api/transactions/checkout/', {'book_id': self.book.id}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_return_increments_copies(self):
        self.client.post('/api/transactions/checkout/', {'book_id': self.book.id}, format='json')
        resp = self.client.post('/api/transactions/return/', {'book_id': self.book.id}, format='json')
        self.assertEqual(resp.status_code, 201)
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_available, 1)
