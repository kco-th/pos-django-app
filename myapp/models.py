from django.db import models
from django.core.exceptions import ValidationError

#re is regular expressions module
import re
from django.db.models import Q
# register
from django.contrib.auth.models import AbstractUser, User

def validate_category_name(value):
    # accept character, number and  (- / _) 
    if not re.match(r'^[a-zA-Z0-9\s\-_]+$', value):
        raise ValidationError("Invalid Category name ")
    
class Category(models.Model):
  name = models.CharField(max_length=100,unique=True, validators=[validate_category_name])
  description = models.CharField(max_length=50,blank=True)
  is_active = models.BooleanField(default=True)
   
#__str__(self) is used to represent a model's objects as a text string.
  def __str__(self):
    return self.name
def validate_name(value):
    # accept character, number and  (- / _) 
    if not re.match(r'^[a-zA-Z0-9\s\-_]+$', value):
        raise ValidationError("Invalid Category name ")
  
class Unit(models.Model):
  name = models.CharField(max_length=100,unique=True, validators=[validate_name])
  description = models.CharField(max_length=50,blank=True)
  
  
#__str__(self) is used to represent a model's objects as a text string.
  def __str__(self):
    return self.name

# product

class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(
       Category,
       on_delete=models.PROTECT,
       related_name='products')
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name='products'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(
      default=5
  )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    @property
    def is_low_stock(self):
        return self.stock <= self.reorder_level


class Sale(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    cash_received = models.DecimalField(max_digits=12, decimal_places=2)
    change = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Sale #{self.id} - {self.total_amount} MMK"

class SaleItem(models.Model):

    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
#Register
class UserProfile(AbstractUser):
  ROLE_CHOICES = (
      ('admin', 'Admin'),
      ('manager', 'Manager'),
      ('cashier', 'Cashier'),
  )
  email = models.EmailField(unique=True)  # Email unique 
  role = models.CharField(
      max_length=20, choices=ROLE_CHOICES, default='cashier'
  )
  def __str__(self):
    return f'{self.username} ({self.get_role_display()})'