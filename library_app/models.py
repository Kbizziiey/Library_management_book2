from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField(null=True, blank=True)
    copies_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    date_of_membership = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    CHECKOUT = 'checkout'
    RETURN = 'return'
    TRANSACTION_TYPE_CHOICES = [
        (CHECKOUT, 'Check Out'),
        (RETURN, 'Return'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} {self.transaction_type} {self.book.title} on {self.date}"
