
from collections import defaultdict
import uuid
from django.shortcuts import render, redirect
from urllib import request
from django.views import View
from . models import Cart, Customer, Product,OrderPlaced
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404



from . forms import CustomerRegistrationForm, CustomerProfileForm

def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title')
        return render (request, "app/category.html", locals())
    

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category = product[0].category).values('title')
        return render(request, "app/category.html", locals())
    
class ProductDetail(View):
    def get(self, request,pk):
        product = Product.objects.get(pk = pk)
        return render(request, "app/productdetail.html", locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Parabéns, cadastro concluido com sucesso")
        else:
            messages.warning(request, "Tipo de dado inválido, tente novamente")
        return render(request,'app/customerregistration.html', locals())
    

class ProfileView(View):
    def get(self, request):
        form  = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user = user, name=name, locality=locality,mobile = mobile, city=city, state=state, zipcode = zipcode)
            reg.save()
            messages.success(request, "Parabéns! Perfil salvo com sucesso")
        else:
            messages.warning(request, "Dados inválidos, tente novamente")
        return render(request, 'app/profile.html', locals())
    
def address(request):
    add = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html', locals())

class updateAdress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Parabéns! Perfil atualizado com sucesso")
        else:
            messages.warning(request, "Tipo de dados inválidos, tente novamente")


        return redirect("address")
    
class UserLogoutView(LogoutView):

    def get(self, request):
        logout(request)
        return redirect('login')

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user , product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user )
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 8
    return render(request, 'app/addtocart.html', locals())

def plus_cart(request):
    if request.method == 'GET':
        
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 8

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 8

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 8

        data={
            
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
class checkout(View):
    def get( self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 8
        return render(request, 'app/checkout.html', locals())
    
def place_order(request):
    if request.method == "POST":
        user = request.user
        custid = request.POST.get('custid')
        customer = Customer.objects.get(id=custid)

        cart_items = Cart.objects.filter(user=user)
        order_uid = uuid.uuid4()  # um ID único para todos os itens deste pedido

        for item in cart_items:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=item.product,
                quantity=item.quantity,
                order_id=order_uid
            )
            item.delete()

        return redirect("orders")




def show_orders(request):
    all_orders = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')

    grouped_orders = defaultdict(list)
    for order in all_orders:
        grouped_orders[order.order_id].append(order)

    # Converter para dict padrão para o template funcionar bem
    grouped_orders = dict(grouped_orders)

    return render(request, 'app/orders.html', {'grouped_orders': grouped_orders})


#def show_orders(request):
   # order_placed = OrderPlaced.objects.filter(user = request.user)
   # return render(request, 'app/orders.html', locals())