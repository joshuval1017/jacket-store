from django.shortcuts import get_object_or_404, render,redirect
from . forms import *
from django.contrib.auth import logout
from . models import *
from django.contrib import messages
import re
from django.utils import timezone
import uuid
from . helpers import *
from datetime import timedelta

from django.db.models import Q 
# Create your views here.
def demo(request):
    return render(request,"myapp/demo.html")
    


def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't immediately save the user
            # Set the first_name and last_name from the form
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()  # Now save the user
            profile=user_details.objects.create(user=user)
            profile.save()
            # Here, you can also log the user in and redirect them as necessary
            coupon_code = str(uuid.uuid4().hex)[:10]  # Random 10-character code
            upto=timezone.now() + timedelta(days=10)
            coupon = Coupon.objects.create(
                code=coupon_code,
                discount_percent=10,
                valid_from=timezone.now(),
                valid_to=upto
            )
            coupon.save()
            valid_to_date = upto.date()
            send_welcome_mail(user.email,coupon_code,valid_to_date)
            return redirect('clothapp:login')
    else:
        form = RegisterForm()
    return render(request, "registration/signup.html", {"form": form})

def custom_logout(request):
    logout(request)
    # Redirect to a specific URL after logout
    return redirect('clothapp:login') 


def index(request):
    products = Product.objects.all()
    cat=Occasion.objects.all()
    context={"a":products,'categories':cat}
    return render(request,"myapp/index.html",context)

def ocassion_products(request,id):
    
    cat=Occasion.objects.get(id=id)
    products=Product.objects.filter(occasion=cat)
    context={"a":products,'cat':cat,'search':False}
    return render(request,"myapp/categoryProducts.html",context)

def search_results(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(Q(name__icontains=query) |Q(description__icontains=query)| Q(occasion__name__icontains=query) | Q(color__name__icontains=query) | Q(material__name__icontains=query))

        
    else:
        results = []
    return render(request, 'myapp/categoryProducts.html', {'a': results, 'cat': query,'search':True})


def profile(request):
    
    a = Product.objects.all()
    has_shipping_address = False
    context= {"a":a,
              "has_shipping_address": has_shipping_address,}
    return render(request,'myapp/profile.html',context)


def EditProfile(request):
  
   
        user = request.user
        

        if request.method == 'POST':
            # Extract form data
            firstName = request.POST.get('first_name')
            lastName = request.POST.get('last_name')
            email = request.POST.get('email')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
            
            # Validation patterns
            nameRegex = re.compile(r'^[A-Za-z\s]+$')
            emailRegex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
            passwordRegex = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')
            # Validation
            errors = {}
            if not nameRegex.match(firstName):
                errors['firstName_error'] = 'Invalid first name.'
            if not nameRegex.match(lastName):
                errors['lastName_error'] = 'Invalid last name.'
            if not emailRegex.match(email):
                errors['email_error'] = 'Invalid email address.'
            if new_password and confirm_new_password:
                if new_password != confirm_new_password:
                    errors['password_match_error'] = 'Passwords do not match.'
                elif not passwordRegex.match(new_password):
                    errors['password_complexity_error'] = 'Password does not meet complexity requirements.'

            if errors:
                return render(request, "myapp/EditProfile.html", {
                    'a': user,
                    'errors': errors
                })

            # Update the user details
            user.first_name = firstName
            user.last_name = lastName
            user.email = email
           
            user.password = new_password
            user.save()
           

            messages.success(request, 'Profile successfully updated.')
            return redirect('clothapp:EditProfile')  # Adjust as needed

        context = {"a": user}
        return render(request, "myapp/EditProfile.html", context)
def AdminLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=Supplier.objects.filter(username=username,password=password)
        
        # Check if the credentials match
        if Admin_login.objects.filter(username=username,password=password).exists():
            # Redirect to the dashboard URL. Replace 'dashboard_url_name' with the actual name of your dashboard URL
            return redirect('clothapp:dashboard')
        elif user.exists():
            request.session['user_id']=user[0].id
            return redirect('clothapp:supplier_home')
        else:
            # Optional: Add some logic to handle incorrect credentials, such as displaying an error message
            return redirect('clothapp:AdminLogin')
    
    # If not a POST request, or the credentials are incorrect, render the login page again
    return render(request,'myapp/AdminLogin.html')


def dashboard(request):
    orders = 2
    total_orders = 10
    total_products = Product.objects.count()
    context = {"b":orders,"a": total_orders,"c":total_products}
    return render(request,"myapp/Admindashboard.html",context)

def productDetail(request,id):
    products = Product.objects.get(id=id)
    context={"product":products}
    return render(request,"myapp/ProductDetail.html",context)



def AddProduct(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        material_id = request.POST.get('material')
        color_id = request.POST.get('color')
        occasion_id = request.POST.get('occasion')
        price = request.POST.get('price')
        sup = request.POST.get('sup')
        
        description = request.POST.get('description')
        supplier=Supplier.objects.get(id=sup)

        material = Material.objects.get(pk=material_id)
        color = Color.objects.get(pk=color_id)
        occasion = Occasion.objects.get(pk=occasion_id)

        product = Product.objects.create(
            name=name,
            image=image,
            material=material,
            color=color,
            occasion=occasion,
            price=price,
            supplier=supplier,
           
            description=description
        )
        product.save()
   
        messages.success(request, 'Product successfully added')

        return redirect('clothapp:viewProducts')
    else:
        materials = Material.objects.all()
        colors = Color.objects.all()
        occasions = Occasion.objects.all()
        sup=Supplier.objects.all()
        return render(request, "myapp/AddProduct.html", {'materials': materials, 'colors': colors, 'occasions': occasions,'sup':sup})

from django.urls import reverse    
def EditProduct(request,product_id):
    product = Product.objects.get(id = product_id) 

    if request.method == 'POST':
        
        product.name = request.POST.get('name')
        product.material_id = request.POST.get('material')
        product.color_id = request.POST.get('color')
        product.occasion_id = request.POST.get('occasion')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        
        # Check if a new image file is uploaded
        if request.FILES.get('new_image'):
            product.image = request.FILES['new_image']
        
        product.save()
        product.save()
        
        return redirect('clothapp:viewProducts')
       
    else:
         materials = Material.objects.all()
         colors = Color.objects.all()
         occasions = Occasion.objects.all()
         return render(request, 'myapp/EditProduct.html',{"up":product,'materials': materials, 'colors': colors, 'occasions': occasions})


  


def productDelete(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    product.delete()
    messages.success(request,"Product deleted successfully")
    return redirect('clothapp:viewProducts')



def viewProducts(request):
    products = Product.objects.all()
   
    total_products = Product.objects.count()
    context = {"products":products,"c":total_products}
    return render(request,"myapp/viewProducts.html",context)


def Sup_dashboard(request):
    id=request.session['user_id']
    supplier=Supplier.objects.get(id=id)
    
    stock = Product.objects.filter(supplier=supplier,stockrequest=True)
    products=Product.objects.filter(supplier=supplier).count()
   
    stocks = stock.count()
    orders = 2
    total_orders = 10
    
    context = {"stock":stocks,"products_supplier":products}
    return render(request,"myapp/SupplierBase.html",context)


def request_stock_update(request, product_id):
    product = Product.objects.get(id=product_id)
    product.stockrequest = True  # Update stock request field to True
    product.save()
    return redirect('clothapp:viewProducts')


def viewSupplierProducts(request):
    id=request.session['user_id']
    supplier=Supplier.objects.get(id=id)
    stock = Product.objects.filter(supplier=supplier,stockrequest=True)
    products_sup=Product.objects.filter(supplier=supplier).count()
   
    stocks = stock.count()
    
    products = Product.objects.filter(supplier=supplier,stockrequest=True)
   
    total_products = products.count()
    context = {"products":products,"c":total_products,"stock":stocks,"products_supplier":products_sup}
    return render(request,"myapp/SupplierViewProducts.html",context)

def user_logout(request):
    del request.session['user_id']
    return redirect('clothapp:AdminLogin')
def update_stock(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        new_stock = request.POST.get('new_stock')
        product.stock = product.stock+int(new_stock)
        product.stockrequest = False  # Reset stock request to False
        product.save()
    return redirect('clothapp:supplierproducts')



def mycart(request):
    
    up = request.user
    cart_id = request.session.get('cart_id')
    off=True
    total=0
    if cart_id:
        cart1 = cart.objects.get(id=cart_id)
        total=cart1.total
        if 'coupon_id' in request.session:
            coupon_id = request.session['coupon_id']
            coupon = Coupon.objects.get(id=coupon_id)
            discount_amount = (cart1.total * coupon.discount_percent) / 100
            print("discount",discount_amount)
            
            total -= discount_amount
            
         
            off=False
            
           

    else:

        cart1 = None
    
    context = {'cart': cart1,'u':up,'coupon_applied':off,'total':total}   
    return render(request, 'myapp/mycart.html', context)


from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def addtocart(request, id):
    if request.method=="POST":
        

        product_obj = Product.objects.get(id=id)

        # check if the cart exists

        cart_id = request.session.get('cart_id')
        if cart_id:
            size=request.POST["size"]

            cart_obj = cart.objects.get(id=cart_id)
            product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj,size=size)
            # item already exist in cart
            if product_in_cart.exists():
                cartproduct = product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
                
            else:
                size=request.POST["size"]
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.price,
                                                        quantity=1, subtotal=product_obj.price,size=size)
                cart_obj.total += product_obj.price
                cart_obj.save()
        else:
            
            up = request.user


            cart_obj = cart.objects.create(customer=up,total=0)
            request.session['cart_id'] = cart_obj.id
            size=request.POST["size"]
            print("size",size)
            print("new cart")
            cp = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1,
                                                    subtotal=product_obj.price,size=size)
            cart_obj.total += product_obj.price
            cart_obj.save()
        
        messages.info(request,"Added To Cart")
        return redirect("/")
    else:
        return redirect("/")


def managecart(request, id):
    print("im in manage cart")
    action = request.GET.get("action")
    cp_obj = CartProduct.objects.get(id=id)
    cart_obj = cp_obj.cart

    if action == "inc":
        if cp_obj.quantity < cp_obj.product.stock:
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        else:
            messages.error(request, "Product quantity exceeds available stock.")
    elif action == "dcr":
        cp_obj.quantity -= 1
        cp_obj.subtotal -= cp_obj.rate
        cp_obj.save()
        cart_obj.total -= cp_obj.rate
        cart_obj.save()
        if cp_obj.quantity == 0:
            cp_obj.delete()
            del request.session['cart_id']
            if 'coupon_id' in request.session and cart_obj.total==0:
                del request.session['coupon_id']


    elif action == 'rmv':
        cart_obj.total -= cp_obj.subtotal
        cart_obj.save()
        cp_obj.delete()
        if 'coupon_id' in request.session and cart_obj.total==0:
            
            del request.session['coupon_id']
    else:
        pass

    return redirect('/my-cart')

def emptycart(request):
    cart_id=request.session.get("cart_id",None)
    cart1=cart.objects.get(id=cart_id)
    cart1.cartproduct_set.all().delete()
    cart1.total=0
    cart1.save()
    if 'coupon_id' in request.session:
        del request.session['coupon_id']

    return redirect('/my-cart')

def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.valid_from <= timezone.now() <= coupon.valid_to:
                request.session['coupon_id'] = coupon.id
                return redirect('/my-cart')
            else:
                # Coupon code has expired
                messages.error(request, 'This coupon code is expired.')
                return redirect('/my-cart')
        except Coupon.DoesNotExist:
            # Coupon code is invalid
            messages.error(request, 'Invalid coupon code.'
                           )
            return redirect('/my-cart')
    return redirect('cart')

def checkout(request):
    
    
    user=request.user
    cart_id = request.session.get("cart_id")
    cart_obj = cart.objects.get(id=cart_id)
    if 'coupon_id' in request.session:
            coupon_id = request.session['coupon_id']
            coupon = Coupon.objects.get(id=coupon_id)
            discount_amount = (cart_obj.total * coupon.discount_percent) / 100
            print("discount",discount_amount)
            
            cart_obj.total -= discount_amount
            cart_obj.save()
  
    if request.method == "POST":
        order_status = "Order recived"

        address = request.POST["address"]
        email=request.POST["email"]

        mobile =request.POST["contact"]
        total = request.POST["total"]
        for cart_product in cart_obj.cartproduct_set.all():
                product = cart_product.product
                product.stock -= cart_product.quantity
                product.save()
        new_order = Orders.objects.create(cart=cart_obj, customer=user, address=address, mobile=mobile,
                                              total=float(total), order_status="order recived")
        new_order.save()
        del request.session['cart_id']
        messages.info(request,f"Order Placed a confirmation mail has been sent to {email}")
        send_order_confirmation_email(email,new_order.id)
        if 'coupon_id' in request.session:
            coupon_id = request.session['coupon_id']
            coupon = Coupon.objects.get(id=coupon_id)
            coupon.delete()
            del request.session['coupon_id']
        return redirect('/')
    else:
        context = {'cart': cart_obj, 'user': user}
        return render(request, './myapp/checkout.html', context)
    

def my_orders(request):
    
    up = request.user
    
    user_orders = Orders.objects.filter(customer=up).order_by('-created_at')

    return render(request, './myapp/my_orders.html', {'user_orders': user_orders})


def display_orders(request):
    orders = Orders.objects.all()
    context = {'orders': orders, 'ORDER_STATUS': ORDER_STATUS}
    return render(request, './myapp/display_orders.html', context)


def update_order_status(request, order_id):
    if request.method == 'POST':
        order = Orders.objects.get(id=order_id)
        new_status = request.POST.get('status')
        order.order_status = new_status
        order.save()
    return redirect('clothapp:display_orders')



from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generate_pdf(request, order_id):
    # Retrieve order details based on order_id
    order = Orders.objects.get(pk=order_id)
    
    # Render HTML template for invoice
    template_path = 'myapp/invoice_template.html'
    context = {'order': order}
    template = get_template(template_path)
    html = template.render(context)
    
    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Return PDF as response
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


#change password
from .helpers import send_forget_password_mail



def ChangePassword(request , token):
    context = {}
    
    
    try:
        profile_obj = user_details.objects.filter(forget_password_token = token).first()
        user=profile_obj.user
        context = {'user_id' : user}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
                         
            
            user_obj = user
            user_obj.set_password(new_password)  # This method hashes the password
            
       
            user_obj.save()
            return redirect('clothapp:login') 
            
            
            
        
        
    except Exception as e:
        print(e)
    return render(request , "./myapp/change-password.html" , context)


import uuid
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            print("inside post")
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username):
                print("no user")
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')
            
            user_obj = User.objects.get(username = username)
            print("user",user_obj)
            token = str(uuid.uuid4())
            profile_obj= user_details.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')
                
    
    
    except Exception as e:
        print(e)
    return render(request ,"./myapp/forget-password.html")
