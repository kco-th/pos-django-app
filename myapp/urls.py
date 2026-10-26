# myapp/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    ProductListCreateAPIView,
    ProductDetailAPIView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = 'myapp'
urlpatterns = [
     #path('', views.home, name='home'),
     path('list', views.product_list, name='list'),
     path('hello/', views.hello, name='hello'),
    # path('api/sample/', views.product_json, name='sample-json'),
     path('<int:product_id>/', views.product_detail, name='detail'),
     path('filter/', views.sample_filter_view, name='filter'),
     path('loop/', views.condition_loop_demo, name='loop'),
     path('student/', views.template_inhertance_demo, name='student'),
     path('upload/', views.static_image, name='upload'),

     #Category 
     path('category/', views.category_list, name='category_list'),
     path('category/<int:pk>/', views.category_detail, name='category_detail'),
     path('category/new/', views.category_create, name='category_create'),
     path('category/<int:pk>/edit/', views.category_update, name='category_update'),
     path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
     # Product
    path('product/',views.product_list,name='product_list'),
    path('product/new/',views.product_create,name='product_create'),
    path('product/<int:pk>/',views.product_detail,name='product_detail'),
    path('product/<int:pk>/edit/',views.product_update,name='product_update'),
    path('product/<int:pk>/delete/',views.product_delete,name='product_delete'),

    path('api/products/',ProductListCreateAPIView.as_view(),name='product-api'),
    path('api/products/<int:pk>/',ProductDetailAPIView.as_view(),name='product-detail-api'),

    # JWT Login
    #Access Token → For using APIs
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    #Refresh Token → For obtaining a new Access Token when the current Access Token expires
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

    #POS
   
    path('dashboard/',views.dashboard_viw,name='dashview_view'),
    path('sidebar/',views.sidebar,name='sidebar_view'),
    path('pos/', views.pos_terminal, name='pos_terminal'),
    path('pos/get-product/', views.get_product_by_code, name='get_product_by_code'),
    path('pos/checkout/', views.checkout_sale, name='checkout_sale'),
    #Inventory
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/update-stock/<int:pk>/',views.update_stock,name='update_stock',
    ),
    #user
    path('register/', views.create_user, name='create_user'),
    #logout
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
]
   

  

#

 
