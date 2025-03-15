from django.db import models
from user.models import UserModel
from books.models import Book

class Order(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    books = models.ManyToManyField(Book, through='OrderItem', related_name='orders')
    '''
    When you use the through parameter in a ManyToManyField, you're telling Django to use an explicit intermediary model—in this case, OrderItem—to manage the relationship between Order and Book (It is a join table). This gives you the flexibility to include extra fields (such as quantity and price) that wouldn't be possible with Django's automatic intermediate table.
    '''
    '''
    Use order.books.all() to get books in an order.
    Use order.order_items.all() to access the extra fields associated with each book in the order.
    '''
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Price per unit at the time of order

    def __str__(self):
        return f"{self.quantity} of {self.book.title} in Order {self.order.id}"

class OrderInvoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=100, unique=True)
    billing_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Additional invoice fields like billing address or tax details can go here

    def __str__(self):
        return f"Invoice {self.invoice_number} for Order {self.order.id}"
