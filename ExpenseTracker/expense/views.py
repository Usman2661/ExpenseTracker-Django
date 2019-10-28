from django.shortcuts import render, redirect
from expense.models import Catagory,Expenses
from Friends.models import Friend,Request
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.db.models import Q
from django.db.models import Sum, Count


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
            checkrequest = Friend.objects.all().filter(Q(UserID_id=UserID)&Q(FriendID_id=UserID))

            if not checkrequest:
                try:
                    CreateFriend = Friend.objects.create(UserID_id=UserID, FriendID_id=UserID)
                except IntegrityError:
                    return redirect('home')
                else:
                    return redirect('home')
            
            MyCatagories = Catagory.objects.filter(Q(User_ID=UserID)|Q(User_ID=0))
            MyExpense = Expenses.objects.all().filter(User_ID_id=UserID)
            context={
                "MyCatagories":MyCatagories,
                "MyExpense":MyExpense,
            }
            return render(request,'expense/home.html',context)
            
               
    else:
        return redirect("login")


def insights(request):
    if request.user.is_authenticated:

        # totalamount = Expenses.objects.raw('SELECT "id", SUM("Amount") as totalexpense from "expense_expenses" ')
        totalusers = User.objects.count()

        # for data in totalamount:
        #     print (data.totalexpense)

        print(totalusers)

        # for data in totalamount:
        #     print(data.totalExpense)
        # print(totalamount.totalExpense)


    


        context={
                "Amounts":totalamount,
                "Users":totalusers,
        }

        return render(request,'expense/insight.html',context)


    else:
        return redirect('login')