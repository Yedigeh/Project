from django.shortcuts import render,redirect
from django.views import View
from . models import Customer, Product, Cart,OrderPlaced,Product
from django.db.models import Count
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response

# Create your views here.
def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
    
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())
    
class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html",locals())
    
#CBV
class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerRegistrationView(View):
    def get(self,request):  
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Вы Успешно Зарегестрированы!")
        else:
            messages.warning(request,"Неправильно Введены Данные!")
        return render(request, 'app/customerregistration.html', locals())  
    
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            city=form.cleaned_data['city']
            phone=form.cleaned_data['phone']
            zipcode=form.cleaned_data['zipcode']

            reg=Customer(user=user,name=name,city=city,phone=phone, zipcode=zipcode)
            reg.save()
            messages.success(request,"Данные Успешно Сохранены")
        else:
            messages.warning(request,"Данные Неправильно Введены")
        return render(request, 'app/profile.html', locals())

def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.city=form.cleaned_data['city']
            add.phone=form.cleaned_data['phone']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Профиль Успешно Обновлен")
        else:
            messages.warning(request,"Данные Неправильно Введены")    
        return redirect("address")

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.price
        amount=amount+value
    totalamount=amount+400
    return render(request, 'app/addtocart.html', locals())

#CBV
class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_item=Cart.objects.filter(user=user)
        famount=0
        for p in cart_item:
            value=p.quantity*p.product.price
            famount=famount+value
        totalamount=famount +400
        return render(request, 'app/checkout.html', locals())

  
def check(request):
    
     user=request.user
     add=Customer.objects.filter(user=user)
     cart_item=Cart.objects.filter(user=user)
   
     famount=0
     for p in cart_item:
        value=p.quantity*p.product.price
        famount=famount+value
        totalamount=famount +400
    # Передать данные в шаблон
     context = {
        'customer_name': user.username,
        'total_price': totalamount,
     }
     return render(request, 'app/check.html', locals())

#FBV
def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart =Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.price
            amount=amount+value
        totalamount=amount+400
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

#FBV   
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart =Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.price
            amount=amount+value
        totalamount=amount+400
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart =Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.price
            amount=amount+value
        totalamount=amount+400
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def search(request):
    query=request.GET['search']
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    product=Product.objects.filter(Q(title__icontains=query))
    return render(request,'app/search.html',locals())