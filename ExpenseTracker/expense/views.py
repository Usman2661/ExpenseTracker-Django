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
from django.db import connection



# Create your views here.

def index(request):

    if request.user.is_authenticated:
        # mydate=request.GET.get('datetimepicker')
       
        
        datetime=request.GET.get('datetimepicker')

        amount=request.GET.get('amount')
        catagory=request.GET.get('catagory')
        contents=request.GET.get('contents')
        notes=request.GET.get('notes')

        # def foo():
        #     print(x)

        if datetime is not None:
            datetime=request.GET.get('datetimepicker')
            amount=request.GET.get('amount')
            catagory=request.GET.get('catagory')
            contents=request.GET.get('contents')
            notes=request.GET.get('notes')
            UserID=request.user.id

       

            expense = Expenses.objects.create(Amount=amount, Catagory=catagory, Contents=contents,Notes=notes,User_ID_id=UserID,Date_Time=datetime)
            expense.save()

            return redirect('home')
            # try:
            #     expense = Expenses.objects.create(Amount=amount, Catagory=catagory, Contents=contents,Notes=notes,User_ID_id=UserID)
            # except IntegrityError:
            #     messages.error(request,'Error: There has been an error while adding expense')
            #     return redirect('home')
            # else:
            #     messages.success(request,'Expense Added Succesfully')
            #     return redirect('home')

        elif request.method=='POST':
            if "newcatagory" in request.POST:
                newcatagory = request.POST['newcatagory']
                UserID=request.user.id

                try:
                    catagory = Catagory.objects.create(Name=newcatagory,User_ID=UserID)
                except IntegrityError:
                    messages.error(request,'Error: There has been an error while adding catagory')
                    return redirect('home')
                else:
                    messages.success(request,'Catagory Added Succesfully')
                    return redirect('home')
        else:
            UserID=request.user.id
            # checkrequest = Friend.objects.all().filter(Q(UserID_id=UserID)&Q(FriendID_id=UserID))

            # if not checkrequest:
            #     try:
            #         CreateFriend = Friend.objects.create(UserID_id=UserID, FriendID_id=UserID)
            #     except IntegrityError:
            #         return redirect('home')
            #     else:
            #         return redirect('home')
            
            MyCatagories = Catagory.objects.filter(Q(User_ID=UserID)|Q(User_ID=0))
            MyExpense = Expenses.objects.all().filter(User_ID_id=UserID).order_by('-id')
            context={
                "MyCatagories":MyCatagories,
                "MyExpense":MyExpense,
            }
            return render(request,'expense/home.html',context)
            
               
    else:
        return redirect("login")


def insights(request):
    if request.user.is_authenticated:


        UserID=request.user.id

        cursor = connection.cursor()
        cursor1 = connection.cursor()
        cursor2 = connection.cursor()

        cursor.execute('SELECT SUM("Amount") as totalexpense from "expense_expenses" ')
        max_value = cursor.fetchone()[0]

        
        cursor1.execute('SELECT COUNT ( DISTINCT "Name" ) AS "Catagories" FROM "expense_catagory"; ')
        totalcatagories = cursor1.fetchone()[0]

        cursor2.execute('SELECT SUM ("Amount" ) AS mytotalexpense FROM "expense_expenses" WHERE "User_ID_id"='+str(UserID)+';' )
        totalspending = cursor2.fetchone()[0]

        totalusers = User.objects.count()


        print(max_value)
        print(totalcatagories)



        # for data in totalamount:
        #     print (data.totalexpense)

        # for data in totalcatagories:
        #      print(data.mycat)
        # print(totalamount.totalExpense)

        # print(totalcatagories.mycat)

        context={
                "Amounts":max_value,
                "Users":totalusers,
                "Catagories":totalcatagories,
                "MySpending":totalspending,
        }

        return render(request,'expense/insight.html',context)


    else:
        return redirect('login')