from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import *
from .form import *


from .form import CreateUserForm
# Create your views here.
#login_required(login_url='login')

def app(request):
    funds = Fund.objects.all()
    return render(request, 'user/index.html',{'funds':funds})


def loginPage(request):
    if request.method == 'POST':
        username =    request.POST.get('username')
        password =    request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect ("/home")
        else:
            messages.error(request,"Invalid  password.")

    context = {}
    return render(request, 'user/login.html',context)

def register(request):
   form = CreateUserForm()
   if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            userName=form.cleaned_data.get('username')
            messages.success(request,"Account has been Created Succefully Welcome "+userName)
            return redirect('/login')
        

   context = {'form':form}

   return render(request, 'user/register.html',context)


def LogUserOut(request):
    logout(request)
    return redirect('/login')


"""
def register(request):
   form = CreateUserForm()
   if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('login.html')

   context = {'form':form}

   return render(request, 'user/register.html',context)

   def register(request):
    SignedUser=CreateUserForm(request.POST)
    if SignedUser.is_valid():
         SignedUser.save()
         userName=SignedUser.cleaned_data.get('username')
         messages.success(request,"account has been created for"+userName)
         return redirect('login.html')
    SignedUser=CreateUserForm()
    return render(request,'user/register.html',{"form":SignedUser})
"""

def fundList(request):  
    funds = Fund.objects.filter(user=request.user.id).values()  
    return render(request,"user/fund_list.html",{'funds':funds})

def fundCreate(request):  
    if request.method == "POST":  
        form = FundForm(request.POST,request.FILES)
        if form.is_valid():  
            try:  
                instance = form.save(commit=False) 
                instance.user = request.user
                instance.save()
                form.save() 
                model = form.instance
                return redirect('/fund-list')  
            except:  
                pass  
    else:  
        form = FundForm()  
    return render(request,'user/fund_create.html',{'form':form}) 

def fundUpdate(request, id):  
    fund = Fund.objects.get(id=id)
    form = FundForm(initial={'title': fund.title, 'description': fund.description, 'author': fund.author, 'year': fund.year})
    if request.method == "POST":  
        form = FundForm(request.POST, instance=fund)  
        if form.is_valid():  
            try:  
                form.save() 
                model = form.instance
                return redirect('/fund-list')  
            except Exception as e: 
                pass    
    return render(request,'user/fund_update.html',{'form':form})

def fundDelete(request, id):
    fund = Fund.objects.get(id=id)
    try:
        fund.delete()
    except:
        pass
    return redirect('/fund-list')

 
