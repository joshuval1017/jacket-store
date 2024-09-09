from django.urls import path
from . views import *
from . import views
from django.contrib.auth import views as auth_views
app_name = 'clothapp'
urlpatterns = [
    path('',index),
     path('signup/',views.signup,name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
   path('dashboard/',views.dashboard,name='dashboard'),
   path('AdminLogin/', views.AdminLogin,name='AdminLogin'),
    path('EditProfile/',views.EditProfile,name='EditProfile'), 
  path('AddProduct',views.AddProduct,name='AddProduct'),
    path('editproduct/<int:product_id>/',views.EditProduct,name="editproduct"),
    path('delete_product/<int:product_id>/', views.productDelete, name='delete_product'),
    path("viewProducts",views.viewProducts,name="viewProducts"),
    path('supplier_home',views.Sup_dashboard,name="supplier_home"),
    path('request-stock-update/<int:product_id>/', views.request_stock_update, name='request_stock_update'),
    path('supplierlogout',views.user_logout,name="supplierlogout"),
    path('supplierproducts',views.viewSupplierProducts,name="supplierproducts"),
     path('update-stock/<int:product_id>/', views.update_stock, name='update_stock'),
     path('productDetail/<int:id>',views.productDetail,name="productDetail"),

      path('my-cart',views.mycart, name='my-cart'),

   path('managecart/<int:id>/',views.managecart,name="managecart"),

   path("empty-cart/",views.emptycart),

   path("checkout",views.checkout),
 path('addtocart/<int:id>/', views.addtocart, name='addtocart'),
path('my-orders',views.my_orders,name='my-orders'),
path('display-orders', views.display_orders, name='display_orders'),
path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
  path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
  path('occasion/<int:id>',views.ocassion_products),
  path('search/', views.search_results, name='search_results'),
  path('download-invoice/<int:order_id>/', views.generate_pdf, name='download_invoice'),
   path('forget-password/' , views.ForgetPassword , name="forget_password"),
       path('change-password/<str:token>/' , views.ChangePassword , name="change_password"),
]
