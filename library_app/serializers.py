from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Member, Transaction

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'copies_available']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'user', 'date_of_membership', 'active']

class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Book.objects.all(), source='book')

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'book_id', 'transaction_type', 'date', 'due_date']
        read_only_fields = ['id', 'user', 'book', 'date']
