from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user.models import UserModel
from books.models import Book
from .models import *
from .serializers import *

class OrderAPIView(APIView):
    """
    API view to handle orders:
     - POST: Place a new order.
     - GET: Retrieve order(s). If email and password are provided as query params, return that user's orders.
     - PUT: Update an existing order. (Requires order_id, email, password, and new books list.)
     - DELETE: Cancel (delete) an order. (Requires order_id, email, password.)
    """

    def authenticate_user(self, email, password):
        try:
            user = UserModel.objects.get(email=email)
            if user.password == password:
                return user
        except UserModel.DoesNotExist:
            return None
        return None
    
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = self.authenticate_user(email, password)
            if not user:
                return Response({"error":"Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
            
            books_data = serializer.validated_data.get("books")

            order = Order.objects.create(user=user)
            total_amount = 0

            for item in books_data:
                isbn = item.get("isbn")
                quantity = item.get("quantity")
                try:
                    book = Book.objects.get(isbn=isbn)
                except Book.DoesNotExist:
                    order.delete()
                    return Response({"error": f"Book with ISBN {isbn} does not exist."},status=status.HTTP_400_BAD_REQUEST)
                
                price = book.price
                total_amount += price * quantity
                OrderItem.objects.create(order=order, book=book, quantity=quantity, price=price)

            invoice_number = f"INV{order.id}"
            OrderInvoice.objects.create(order=order, invoice_number=invoice_number, total_amount=total_amount)

            order_detail_serializer = OrderDetailSerializer(order)
            return Response(order_detail_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # If email and password are provided as query parameters, filter orders for that user.
        email = request.query_params.get('email')
        password = request.query_params.get('password')
        if email and password:
            user = self.authenticate_user(email, password)
            if not user:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
            orders = Order.objects.filter(user=user)
        else:
            orders = Order.objects.all()
            
        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # Update an existing order. order_id must be provided.
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            order_id = serializer.validated_data.get('order_id')
            
            if not order_id:
                return Response({"error": "order_id is required for update"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = self.authenticate_user(email, password)
            if not user:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                order = Order.objects.get(id=order_id, user=user)
            except Order.DoesNotExist:
                return Response({"error": "Order not found for this user"}, status=status.HTTP_404_NOT_FOUND)
            
            # Remove existing order items and invoice (if any)
            order.order_items.all().delete()
            if hasattr(order, 'invoice'):
                order.invoice.delete()
            
            books_data = serializer.validated_data.get('books')
            total_amount = 0
            for item in books_data:
                isbn = item.get('isbn')
                quantity = item.get('quantity')
                try:
                    book = Book.objects.get(isbn=isbn)
                except Book.DoesNotExist:
                    return Response({"error": f"Book with ISBN {isbn} does not exist."},
                                    status=status.HTTP_400_BAD_REQUEST)
                price = book.price
                total_amount += price * quantity
                OrderItem.objects.create(order=order, book=book, quantity=quantity, price=price)
            
            invoice_number = f"INV{order.id}"
            OrderInvoice.objects.create(order=order, invoice_number=invoice_number, total_amount=total_amount)
            
            order_detail_serializer = OrderDetailSerializer(order)
            return Response(order_detail_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Cancel an order. Requires email, password, and order_id.
        email = request.data.get('email')
        password = request.data.get('password')
        order_id = request.data.get('order_id')
        
        if not (email and password and order_id):
            return Response({"error": "email, password and order_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = self.authenticate_user(email, password)
        if not user:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found for this user"}, status=status.HTTP_404_NOT_FOUND)
        
        order.delete()
        return Response({"message": "Order deleted successfully"}, status=status.HTTP_200_OK)

'''
{
  "email":"sivanaran@gmail.com",
  "password":"password",
  "books":[{
    "isbn":"9780743273565",
    "quantity":2
  },
  {
    "isbn":"1234567890",
    "quantity":3
  }]
}
'''