from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
 
# Create your views here.


def store(request):

    if request.user.is_authenticated:
        customer=request.user.customer
        order, created =Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        #for dispalying the number above the cart icon on index inheirted from order which as an object of Order named as orded above
        cartItems=order.get_order_total
    else:
        items=[]
        order = {'get_order_total' : 0, 'get_order_items' : 0, 'shipping' : False}
        #for dispalying the number above the cart icon on index
        cartItems=order['get_order_total']


    products=Product.objects.all()
    context = { 'products' : products, 'cartItems' : cartItems}
    return render(request, 'store/Store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created =Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems=order.get_order_total
    else:
        items=[]
        order = {'get_order_total' : 0, 'get_order_items' : 0, 'shipping' : False}
        cartItems=order['get_order_total']

    context={'items': items, 'order': order, 'cartItems' : cartItems}
    return render(request, 'store/Cart.html', context)
 

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created =Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems=order.get_order_total
    else:
        items=[]
        order = {'get_order_total' : 0, 'get_order_items' : 0, 'shipping' : False}
        cartItems=order['get_order_total']
    return render(request, 'store/Checkout.html', {'items' : items, 'order' : order, 'cartItems' : cartItems})


def updateItem(request):
    data = json.loads(request.body)
    productId= data['productId']
    action = data['action']
    print('ProductId', productId)
    print('Action:', action)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created =Order.objects.get_or_create(customer=customer, completed=False)
    orderItem, created=OrderItem.objects.get_or_create(order=order, product=product)
    #action from above
    if action == 'add':
        orderItem.quantity= (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity= (orderItem.quantity-1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.view.now().timestamp()
    data = json.load(request.body)


    if request.user.is_autheticated:
        customer=request.user.customer
        order, created =Order.objects.get_or_create(customer=customer, completed=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if  total == order.get_order_items:
            order.completed = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shiping']['address'],
                citu=data['shiping']['city'],
                state=data['shiping']['state'],
                zipcode=data['shiping']['zipcode'],
            )

    else:
        print('user not logged in')
    return JsonResponse('Payment completed', safe= False)
    