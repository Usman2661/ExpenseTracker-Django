import json
from django.shortcuts import render , redirect
from django.contrib.auth.models import User,auth
from django.db.models import Q
from django.db import IntegrityError
from django.contrib import messages
from Friends.models import Request,Friend
from api.models import Passenger
from django.db.models import Count,Sum
from django.http import JsonResponse
from datetime import datetime
from expense.models import Expenses
from django.utils.dateparse import parse_date
import requests

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            MyID=request.user.id
            FriendID=request.POST['UserID']
            print(FriendID)

            try:
                FriendAdded = Friend.objects.create(UserID_id=MyID, FriendID_id=FriendID)
                FriendAddedToOther = Friend.objects.create(UserID_id=FriendID, FriendID_id=MyID)
                RequestUpdate = Request.objects.filter(Q(SentBy_id=FriendID)&Q(SentTo_id=MyID)).update(Status=True)
            except IntegrityError:
                messages.error(request,'Error: There has been an error while adding friend')
                return redirect('friends')
            else:
                messages.success(request,'Friend Added Succesfully')
                return redirect('friends')
        else:

            MyUserID=request.user.id
            #myrequests=User.objects.filter(UserID_SentTo=MyUserID)
            #myrequests = Request.objects.select_related('SentTo').filter(SentTo_id=MyUserID)
            #myrequests.SentTo_id.Username
            #myrequests = User.objects.filter(UserID_SentTo = MyUserID)
            myfriends= Friend.objects.select_related().filter(UserID_id=MyUserID)
            myrequests = Request.objects.select_related().filter(Q(SentTo=MyUserID)&Q(Status=False))

            print(myfriends.query)
            #.values_list('SentBy__username', 'SentBy__first_name','DateTimeSent')
            #username=myrequests.SentBy__username
            #fname=myrequests.SentBy__first_name
            #date=myrequests.DateTimeSent
            #myrequests.SentBy_id
            #myrequests.SentBy
            #myrequests.User.username
            #myrequests.UserID_SentTo.username
            #myrequests.SentTo_id.first_name
            # print(username)
            # print(fname)
            # print(date)

            #sentbyname=myrequests.DateTimeSent
            
            #print(sentbyname)
            print(myrequests)
            # data = []
            # for res in results:

            #     data.append( {
            #         "Name": res.SentBy_id.first_name,
            #         "Email": res.SentBy_id.username,
            #         "DateTimeSent": res.DateTimeSent,
            #         "Status": res.Status,
            #     })
            #myrequests = Request.objects.filter(SentTo_id=MyUserID).values('User__first_name','User__last_name','User__username','DateTimeSent')
            # print(myrequests)
            context={
                'requests':myrequests,
                'friends':myfriends,
            }
            return render(request,"friends/index.html",context)
    else:
        return render('login')


def leaderboards(request):
    if request.user.is_authenticated:
        leaderboard= Expenses.objects.select_related().values('User_ID').annotate(TotalExpense=Sum('Amount')).order_by('-TotalExpense')
        #leaderboard= Expenses.objects.raw('SELECT "expense_expenses.User_ID_id", SUM(expense_expenses.Amount) as TotalExpense FROM expense_expenses Group By User_ID Order by TotalExpense DESC')
        print(leaderboard)
        print(leaderboard.query)
        context={
            'leaderboards':leaderboard,
        }
        return render(request,"friends/leaderboards.html",context)
    else:
        return render('login')

def search(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            SentBy=request.user.id
            SentTo=request.POST['UserID']
            
            checkrequest = Request.objects.all().filter(Q(SentBy_id=SentBy)&Q(SentTo_id=SentTo))

            if not checkrequest:
                print('No Results')
                try:
                    FriendRequest = Request.objects.create(SentBy_id=SentBy, SentTo_id=SentTo)
                except IntegrityError:
                    messages.error(request,'Error: There has been an error while sending request')
                    return redirect('friends')
                else:
                    messages.success(request,'Friend Added Succesfully')
                    return redirect('friends')
            else:
                messages.error(request,'Error: You have already requested to add this user')
                return redirect('friends')
                
        else:
            search=request.GET['search']
            UserID=request.user.id
            result = User.objects.all().filter(Q(first_name__icontains=search)|Q(last_name__icontains=search)|(Q(username__icontains = search )))
            result=result.filter(~Q(id = UserID))
            context = {
                "searchresults":result,
            }
            return render(request,"friends/search.html",context)
    else:
        return render('login')

def chart_data(request):

    time=request.GET.get('time')
    mydate=request.GET.get('mydate')
    #lastconnection = datetime.strptime(mydate, '%d/%m/%Y').strftime('%Y-%m-%d')
   
    ddate=parse_date(mydate)
    theyear = ddate.year
    theday = ddate.day
    themonth = ddate.month
    
    UserID=request.user.id
    if time=='All':
        dataset = Expenses.objects.values('Catagory').annotate(totalExpense=Sum('Amount')).filter(User_ID_id=UserID)
    else:
        dataset = Expenses.objects.values('Catagory').annotate(totalExpense=Sum('Amount')).filter(Q(User_ID_id=UserID)&Q(Date_Time__year=theyear,Date_Time__month=themonth,Date_Time__day=theday))


    #dataset = Expenses.objects.values('Date_Time').annotate(totalExpense=Sum('Amount')).filter(User_ID_id=UserID)
    #print(dataset)


    # dataset2=requests.get('http://localhost:8000/api/expense/')
    # chartdata= dataset2.json()

    # print(chartdata)


    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Spending Catagory Wise'},
        'series': [{
            'name': 'Total Amount',
            'data': list(map(lambda row: {'name': row['Catagory'], 'y': row['totalExpense']}, dataset))
        }]
    }

    return JsonResponse(chart)

def line_chart(request):

    UserID=request.user.id
    dataset = Expenses.objects.values('Date_Time').annotate(totalExpense=Sum('Amount')).filter(User_ID_id=UserID)

    categories = list()
    totalExpense=list()


    for mydata in dataset:
        categories.append(mydata['Date_Time'].date())
        totalExpense.append(mydata['totalExpense'])    

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Spending Date Wise'},
        'xAxis': {'categories': categories},
        'series': [{
            'name': 'Total Amount',
            'data': totalExpense
        }]
    }

    return JsonResponse(chart)
