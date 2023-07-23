import datetime
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.views import View
from . models import *

from django.contrib.auth.models import  User
from .forms import MyUserCreationForm, NoteForm

# Create your views here.
def index(request):

    if request.user.is_authenticated:
        customer =request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all() # type: ignore
        cart_Items = order.get_cart_items
    else:
        items=[]
        order= {'get_cart_items':0,'get_cart_total':0, 'shipping': False}
        cart_Items = order['get_cart_items']


    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)  |
        Q(name__icontains=q)
    )
    rooms_count = rooms.count
    topics = Note.objects.all()[0:5]
    context={'rooms':rooms,'topics':topics,'rooms_count':rooms_count,'cart_Items':cart_Items}
    return render(request,'index.html',context)


@login_required(login_url='login')
def download_section(request,pk):
    rooms = Room.objects.get(id=pk)
    user =  rooms.host
    similarnote = Room.objects.filter(host = user)
    
    context={'rooms':rooms,'similarnote':similarnote}
    return render(request,'download_section.html',context)


def profilePage(request,pk):
    user=User.objects.get(id=pk)
    rooms = user.room_set.all() # type: ignore
    topics=Note.objects.all()
    rooms_count = rooms.count
    context = {'user':user,'rooms':rooms,'topics':topics,'rooms_count':rooms_count}
    return render(request,'profile.html',context)

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'login_register.html', {'form': form})


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'login_register.html', context)




def logoutUser(request):
    logout(request)
    return redirect('home')
    

@login_required(login_url='login')
def createNote(request):
    form = NoteForm()
    topics = Note.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic ,created = Note.objects.get_or_create(name=topic_name)

        Room.objects.get_or_create(
            topic=topic,
            host=request.user,
            name= request.POST.get('name'),
            description= request.POST.get('description'),
            avatar=request.POST.get('avatar'),
            rate=request.POST.get('rate')

        )
        return redirect('home')

    context={'topics':topics,'form':form}
    return render(request, 'create_note.html', context)


def Catagories(request):
    departments = Departments.objects.all()
    context = {'departments':departments}
    return render(request,'catagories.html',context)


def semester(request,pk):
    department = Departments.objects.get(id=pk)
    semesters = department.semester_set.all() # type: ignore
    context = {'semesters':semesters}
    return render(request,'semester.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer =request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all() # type: ignore
        cart_Items = order.get_cart_items
    else:
        items=[]
        order= {'get_cart_items':0,'get_cart_total':0}
        cart_Items = order['get_cart_items']

    context = {'items':items,'order':order,'cart_Items':cart_Items}
    return render(request,'checkout.html',context)



def Cart(request):
    if request.user.is_authenticated:
        customer =request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all() # type: ignore
        cart_Items = order.get_cart_items
    else:
        items=[]
        order= {'get_cart_items':0,'get_cart_total':0,'shipping':False}
        cart_Items = order['get_cart_items']

    context = {'items':items,'order':order,'cart_Items':cart_Items}
    return render(request,'my_cart.html',context)


def updateItem(request):
    
    data = json.loads(request.body)
    print(data)
    productId = data['productId']
    action = data['action']
    print('Action:',action)
    print('Product', productId)

    customer=request.user.customer
    product = Room.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    quantity = 1  # Set a default quantity, which could be updated based on 'action'

    if action == 'add':
    # Increase the quantity by 1 for adding an item to the cart
        quantity = 1
    elif action == 'remove':
    # Decrease the quantity by 1 for removing an item from the cart
        quantity = -1




    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'quantity': quantity})
    if not created:
    # If the OrderItem already exists, update the quantity accordingly
        orderItem.quantity += quantity
        orderItem.save()

# Additional logic to remove the OrderItem if the quantity becomes zero or less
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item added' ,safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                country = data['shipping']['country']
            )
        else:
            print("User is not logged")
    return JsonResponse("Payment done",safe=False)

































