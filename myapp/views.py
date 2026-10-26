from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect,render
# Create your views here.  
from django.http import HttpResponse
from django.http import JsonResponse  
from django.db.models import Q, Sum
from datetime import datetime
from .forms import CategoryForm, CustomUserCreationForm, ProductForm
from .models import Category,Product,Sale, SaleItem
from django.contrib import messages
from django.core.paginator import Paginator
#for REST API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer
#JWT
#from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
#POS
from django.db import transaction
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Sale, SaleItem
import json
from decimal import Decimal
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import F
#hello
def hello(request):  
   return HttpResponse("<h2>Hello, Welcome to Django!</h2>")  

def product_detail(request, product_id):
    return JsonResponse({
        'id': product_id,
        'name': 'Keyboard'
    })
def product_list(request):
    products = [
        {'id': 1, 'name': 'Keyboard', 'price': 45000},
        {'id': 2, 'name': 'Mouse', 'price': 25000},
    ]
    return render(request, 'products/product_list.html', {'products': products})
    

def sample_filter_view(request):
    context = {
        'user_name': 'mg mg',
        'site_title': 'MY ONLINE STORE',
        'bio': '',  # Empty Variable
        'products': [
            {'name': 'Keyboard', 'price': 45000},
            {'name': 'Mouse', 'price': 25000},
            {'name': 'Monitor', 'price': 350000},
        ],
        'today': datetime.now()
    }
    return render(request, 'products/filter_demo.html', context)

def condition_loop_demo(request):
    context = {
        'user_role': 'admin',  # 'admin', 'member',  'guest' 
        'is_logged_in': True,
        'products': [
            {'name': 'Keyboard', 'price': 45000, 'in_stock': True},
            {'name': 'Mouse', 'price': 25000, 'in_stock': True},
            {'name': 'Monitor', 'price': 350000, 'in_stock': False},
        ],
        'empty_list': []  # Empty loop  
    }
    return render(request, 'products/condition_loop.html', context)

def template_inhertance_demo(request):
    context = {
         'students': [
            {'name': 'John', 'age':20},
            {'name': 'Mary', 'age':20},
             
        ],
        'empty_list': []  # Empty loop  
    }
    return render(request, 'student/student_list.html', context)
#static image
def static_image(request):
     return render(request, 'products/static_demo.html')

def bootstrap_demo(request):
     return render(request, 'products/bootstrap_demo.html')



#Category CRUD
# 1. READ: (List View)

def category_list(request):
  category = Category.objects.all()
  return render(request, 'category/category_list.html', {'categories': category})


# 2. READ: Category (Detail View)
def category_detail(request, pk):
  #get_object_or_404(Category, pk=pk) is for display page not found message
  #first pk is Primary Key (Database ID)
  #second pk is url parameter
  categories = get_object_or_404(Category, pk=pk)
  return render(request, 'category/category_confirm_delete.html', {'category': categories}) 


# 3. CREATE: new category
def category_create(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
      form.save() #save new record to table
      return redirect('myapp:category_list')
  else:
    form = CategoryForm() #add empty form
    return render(request, 'category/category_form.html', {'form': form})

# 4. UPDATE: Category
def category_update(request, pk):
  category = get_object_or_404(Category, pk=pk)
  if request.method == 'POST':
    #Only when `instance=category` is included will 
    # the system update the existing category instead of creating a new one.
    form = CategoryForm(request.POST, instance=category)
    if form.is_valid():
      form.save()
      return redirect('myapp:category_list')
  else:
    form = CategoryForm(instance=category)
  return render(
      request, 'category/category_form.html', {'form': form, 'category': category}
  )

# 5. DELETE: category  
def category_delete(request, pk):
  # 1. Retrieve the Category Object for which 'Delete' was clicked.
  category = get_object_or_404(Category, pk=pk)
  # 2. If 'Confirm' (POST) is performed -> Delete the data and display the list again.
  if request.method == 'POST':
    category.delete()
    return redirect('myapp:category_list')
  # 3. If not yet confirmed (GET) -> Displays the confirmation page.
  return render(
      request, 'category/category_confirm_delete.html', {'category': category}
  )
# Product List
def product_list(request):
    products = Product.objects.all()
    return render(request,'product/product_list.html',{'products': products})
      
# Product Create
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:product_list')
    else:
        form = ProductForm()
        return render(request,'product/product_form.html',{'form': form,'title': 'Create Product'})
    
# Product Update
def product_update(request, pk):
    product = get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('myapp:product_list')
    else:
        form = ProductForm(instance=product)
        return render(request,'product/product_form.html',{'form': form,'title': 'Edit Product'})
        
# Product Delete
def product_delete(request, pk):
    product = get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('myapp:product_list')
    return render(request,'product/product_confirm_delete.html',{'product': product})

#REST
class ProductListCreateAPIView(APIView):
     # JWT Login Required
    permission_classes = [IsAuthenticated]
    # http get method
    def get(self, request):
        products = Product.objects.all()
         
        serializer = ProductSerializer(
            products,
            many=True   #many products
        )
        return Response(serializer.data)
    # http post method
    def post(self, request):
        serializer = ProductSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
# class ProductDetailAPIView
class ProductDetailAPIView(APIView):
     # JWT Login Required
    permission_classes = [IsAuthenticated]
    #Searching for an object in the database.
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None
     #Handles the HTTP GET request.   
    def get(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product)
        return Response(serializer.data)
# http put method
    def put(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(
            product,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    # http delete method
    def delete(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
#dashboard
@login_required(login_url='myapp:login')
def dashboard_viw(request):
  #  Stat Cards  Data
  total_revenue = (
      Sale.objects.aggregate(total=Sum('total_amount'))['total'] or 0
  )
  total_orders = Sale.objects.count()
  low_stock_count = Product.objects.filter(stock__lte=F('reorder_level')).count()

  # Chart data (Sales Analytics)
  monthly_sales = (
      Sale.objects.annotate(month=TruncMonth('created_at'))
      .values('month')
      .annotate(total=Sum('total_amount'))
      .order_by('month')
  )

  chart_labels = [item['month'].strftime('%b') for item in monthly_sales]
  chart_data = [float(item['total']) for item in monthly_sales]

 
  # 3. The 5 most recent transactions (fetching Sale, SaleItem, and Product data using prefetch)
  recent_sales = Sale.objects.prefetch_related('items__product').order_by(
      '-created_at'
  )[:5]

  context = {
      'total_revenue': total_revenue,
      'total_orders': total_orders,
      'low_stock_count': low_stock_count,
      'chart_labels': json.dumps(chart_labels),
      'chart_data': json.dumps(chart_data),
      'recent_sales': recent_sales,
  }
  return render(request, 'dashboard/dashboard.html', context)

#Sidebar
def sidebar(request):
    return render(request, 'includes/sidebar.html')

#Register
def register(request):
    # When data is submitted from a form (POST method)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save() # save new User  
            messages.success(request, 'Account creation successful. Please log in.')
            return redirect('myapp:login') # Login page
    # When accessing the page normally (GET method)
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

#login
#def login(request):
 #   return render(request, 'auth/login.html')

#POS
@ensure_csrf_cookie
def pos_terminal(request):
    # stock__gt=0 is stock >0
    # read data from products table for sale 
    products = Product.objects.filter(stock__gt=0)
    #order_by('-created_at')= (-) is decending order by created_at,[:10] Top ten sale reacord
    recent_sales = Sale.objects.order_by('-created_at')[:10]
    return render(request, 'pos/pos.html')
   
def get_product_by_code(request):
    '''API to search for a product by entering an Item Code (Product ID)'''
    code = request.GET.get('code', '').strip() #remove space
    print(code)
    try:
        product = Product.objects.get(id=code, is_active=True)
        if product.stock <= 0:
            return JsonResponse({'success': False, 'message': 'Product is out of stock'})
        return JsonResponse({
                'success': True,
                'product': {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'stock': product.stock
                }
            })
    except (Product.DoesNotExist, ValueError):
        return JsonResponse({'success': False, 'message': 'Product not found'})

#Check out
def checkout_sale(request):
    '''Save voucher'''
    if request.method == 'POST':
        data = json.loads(request.body)
        items = data.get('items', [])
        cash_received = Decimal(str(data.get('cash_received', 0)))

        if not items:
            return JsonResponse({'success': False, 'message': 'no data '})

        try:
            #transaction.atomic() is commit or cancel for all db operation 
            with transaction.atomic():
                total_amount = Decimal('0.00')
                sale_items_to_create = []

                # Calculate stock balance
                for item in items:
                    # update stock balance
                    product = Product.objects.select_for_update().get(id=item['id'])
                    qty = int(item['quantity'])
                    
                    if product.stock < qty:
                        return JsonResponse({
                            'success': False, 
                            'message': f"{product.name} insuffeint balance  {product.stock})"
                        })

                    subtotal = product.price * qty
                    total_amount += subtotal

                    # decreass stock  
                    product.stock -= qty
                    product.save()

                    sale_items_to_create.append({
                        'product': product,
                        'quantity': qty,
                        'unit_price': product.price,
                        'subtotal': subtotal
                    })

                if cash_received < total_amount:
                    return JsonResponse({'success': False, 'message': 'not enough payment'})

                change = cash_received - total_amount

                # save new Sale voucher  
                sale = Sale.objects.create(
                    total_amount=total_amount,
                    cash_received=cash_received,
                    change=change
                )

                # save SaleItem  
                for item_data in sale_items_to_create:
                    SaleItem.objects.create(
                        sale=sale,
                        product=item_data['product'],
                        quantity=item_data['quantity'],
                        unit_price=item_data['unit_price'],
                        subtotal=item_data['subtotal']
                    )

                return JsonResponse({
                    'success': True,
                    'sale_id': sale.id,
                    'total_amount': float(total_amount),
                    'change': float(change),
                    'message': 'saving is success'
                })

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

#Inventory
def inventory_list(request):
   query = request.GET.get('q', '')
   products = Product.objects.all().select_related('category').order_by('name')
   categories = Category.objects.all()

   return render(
      request,
      'inventory/inventory_list.html',
      {
          'products': products,
          'categories': categories,
          'query': query,
       },
  )

def update_stock(request, pk):
  if request.method == 'POST':
    product = get_object_or_404(Product, pk=pk)
    add_qty = int(request.POST.get('quantity', 0))

    if add_qty > 0:
      product.stock += add_qty
      product.save()
      messages.success(
          request, f'{product.name} for Stock {add_qty} added'
      )

  return redirect('myapp:inventory_list')    

#Create User
def create_user(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      messages.success(
          request, 'Saving is success'
      )
      return redirect('myapp:create_user')
  else:
    form = CustomUserCreationForm()

  return render(request, 'auth/create_user.html', {'form': form})

#logout

def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out of the account.")
    return redirect('myapp:login')  # return to Login  

#login
def user_login(request):
    # If already logged in, redirect to the inventory or designated page.
    if request.user.is_authenticated:
        return redirect('myapp:inventory_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Redirecting to the intended original URL if a 'next' parameter is present
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('myapp:inventory_list')
        else:
            messages.error(request, 'Username or  Password wrong')
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})