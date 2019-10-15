from django.shortcuts import render, redirect
from expense.models import Catagory,Expenses
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.db.models import Q
from django.db.models import Sum


# Create your views here.

def index(request):

    if request.user.is_authenticated:

        if request.method=='POST':
            if "newcatagory" not in request.POST:
                amount=request.POST['amount']
                catagories=request.POST['catagory']
                content=request.POST['content']
                notes=request.POST['notes']
                UserID=request.user.id

                try:

                    expense = Expenses.objects.create(Amount=amount, Catagory=catagories, Contents=content,Notes=notes,User_ID_id=UserID)
            # status=user.save()
                except IntegrityError:
                    messages.error(request,'Error: There has been an error while adding expense')
                    return redirect('home')
                else:
                    messages.success(request,'Expense Added Succesfully')
                    return redirect('home')
            else:
                newcatagory = request.POST['newcatagory']
                UserID=request.user.id

                try:
                    catagory = Catagory.objects.create(Name=newcatagory,User_ID=UserID)
            # status=user.save()
                except IntegrityError:
                    messages.error(request,'Error: There has been an error while adding catagory')
                    return redirect('home')
                else:
                    messages.success(request,'Catagory Added Succesfully')
                    return redirect('home')



        else:
            UserID=request.user.id
            MyCatagories = Catagory.objects.filter(Q(User_ID=UserID)|Q(User_ID=0))
            MyExpense = Expenses.objects.all().filter(User_ID_id=UserID)
            # MyGraph = Expenses.objects.values('')
            print(MyCatagories)
            print(MyExpense)
            context={
                "MyCatagories":MyCatagories,
                "MyExpense":MyExpense,
            }
            return render(request,'expense/home.html',context)

    else:
        return redirect("login")
