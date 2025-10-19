from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Book, Member, Transaction
from .serializers import BookSerializer, MemberSerializer, TransactionSerializer, UserSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        available = self.request.query_params.get('available')
        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        isbn = self.request.query_params.get('isbn')

        if available is not None:
            if available.lower() in ['1', 'true', 'yes']:
                qs = qs.filter(copies_available__gt=0)
            else:
                qs = qs.filter(copies_available__lte=0)
        if title:
            qs = qs.filter(title__icontains=title)
        if author:
            qs = qs.filter(author__icontains=author)
        if isbn:
            qs = qs.filter(isbn__icontains=isbn)
        return qs

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related('user').all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.select_related('user', 'book').all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=user)

    @action(detail=False, methods=['post'], url_path='checkout')
    @db_transaction.atomic
    def checkout(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'detail': 'book_id required'}, status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Book, pk=book_id)

        if book.copies_available < 1:
            return Response({'detail': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)

        already_checked_out = Transaction.objects.filter(user=user, book=book, transaction_type=Transaction.CHECKOUT).exists()
        if already_checked_out:
            return Response({'detail': 'User already has this book checked out'}, status=status.HTTP_400_BAD_REQUEST)

        book.copies_available -= 1
        book.save()
        transaction = Transaction.objects.create(user=user, book=book, transaction_type=Transaction.CHECKOUT)
        serializer = TransactionSerializer(transaction, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='return')
    @db_transaction.atomic
    def return_book(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'detail': 'book_id required'}, status=status.HTTP_400_BAD_REQUEST)
        book = get_object_or_404(Book, pk=book_id)

        checked_out = Transaction.objects.filter(user=user, book=book, transaction_type=Transaction.CHECKOUT)
        if not checked_out.exists():
            return Response({'detail': 'No checkout record found for this user and book'}, status=status.HTTP_400_BAD_REQUEST)

        book.copies_available += 1
        book.save()
        transaction = Transaction.objects.create(user=user, book=book, transaction_type=Transaction.RETURN)
        serializer = TransactionSerializer(transaction, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
