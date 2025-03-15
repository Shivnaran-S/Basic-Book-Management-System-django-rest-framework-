from rest_framework import serializers
from .models import *

class BookOrderSerializer(serializers.Serializer):
    isbn = serializers.CharField()
    quantity = serializers.IntegerField()

class OrderSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    # order_id is only needed for updates (PUT) and deletes.
    order_id = serializers.IntegerField(required=False)
    books = BookOrderSerializer(many=True)

# Serializers for returning order details

class OrderItemDetailSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['book_name', 'quantity']

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInvoice
        fields = ['invoice_number', 'billing_date', 'total_amount']

class OrderDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    order_items = OrderItemDetailSerializer(many=True, read_only=True)
    invoice = InvoiceSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user_name', 'order_date', 'order_items', 'invoice']
