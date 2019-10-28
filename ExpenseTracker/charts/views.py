from django.shortcuts import render
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
import datetime
from expense.models import Expenses
from django.utils.dateparse import parse_date
import requests

# Create your views here.

def chart_data(request):

    time=request.GET.get('time')
    mydate=request.GET.get('mydate')
    mydate1=request.GET.get('mydate1')
    #lastconnection = datetime.strptime(mydate, '%d/%m/%Y').strftime('%Y-%m-%d')
   
    ddate=parse_date(mydate)
    theyear = ddate.year
    theday = ddate.day
    themonth = ddate.month

    ddate1=parse_date(mydate1)
    theyear1 = ddate1.year
    theday1 = ddate1.day
    themonth1 = ddate1.month

    first_date = datetime.date(theyear, themonth, theday)
    last_date = datetime.date(theyear1, themonth1, theday1)
    
    UserID=request.user.id
    if time=='All':
        dataset = Expenses.objects.values('Catagory').annotate(totalExpense=Sum('Amount')).filter(User_ID_id=UserID)
    else:
        dataset = Expenses.objects.values('Catagory').annotate(totalExpense=Sum('Amount')).filter(Q(User_ID_id=UserID)&Q(Date_Time__range=(first_date, last_date)))

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

    time=request.GET.get('time')
    mydate=request.GET.get('mydate')
    mydate1=request.GET.get('mydate1')
    #lastconnection = datetime.strptime(mydate, '%d/%m/%Y').strftime('%Y-%m-%d')
   
    ddate=parse_date(mydate)
    theyear = ddate.year
    theday = ddate.day
    themonth = ddate.month

    ddate1=parse_date(mydate1)
    theyear1 = ddate1.year
    theday1 = ddate1.day
    themonth1 = ddate1.month

    first_date = datetime.date(theyear, themonth, theday)
    last_date = datetime.date(theyear1, themonth1, theday1)

    UserID=request.user.id
    if time=='All':
        dataset = Expenses.objects.values('Date_Time__date').annotate(totalExpense=Sum('Amount')).filter(User_ID_id=UserID)
    else:
        dataset = Expenses.objects.values('Date_Time__date').annotate(totalExpense=Sum('Amount')).filter(Q(User_ID_id=UserID)&Q(Date_Time__range=(first_date, last_date)))

    categories = list()
    totalExpense=list()

    for mydata in dataset:
        categories.append(mydata['Date_Time__date'])
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


def pie_chart_leaderboard(request):

    # time=request.GET.get('time')
    # mydate=request.GET.get('mydate')
    # mydate1=request.GET.get('mydate1')
    # #lastconnection = datetime.strptime(mydate, '%d/%m/%Y').strftime('%Y-%m-%d')
   
    # ddate=parse_date(mydate)
    # theyear = ddate.year
    # theday = ddate.day
    # themonth = ddate.month

    # ddate1=parse_date(mydate1)
    # theyear1 = ddate1.year
    # theday1 = ddate1.day
    # themonth1 = ddate1.month

    # first_date = datetime.date(theyear, themonth, theday)
    # last_date = datetime.date(theyear1, themonth1, theday1)
    
    UserID=request.user.id
    # if time=='All':
    #     dataset = Expenses.objects.values('Catagory').annotate(totalExpense=Sum('Amount')).filter(User_ID_id=UserID)
    # else:
    dataset =  Expenses.objects.raw('''SELECT "expense_expenses"."User_ID_id","auth_user"."id","auth_user"."first_name", "auth_user"."last_name", SUM("expense_expenses"."Amount") AS "TotalExpense" FROM "expense_expenses" INNER JOIN "Friends_friend" ON ("expense_expenses"."User_ID_id"="Friends_friend"."FriendID_id") INNER JOIN auth_user ON  ("expense_expenses"."User_ID_id"="auth_user"."id") WHERE "Friends_friend"."UserID_id"=%s GROUP BY "expense_expenses"."User_ID_id","auth_user"."id" ORDER BY "TotalExpense" DESC''',[UserID])
    print(dataset)

    names = list()
    totalExpense=list()

    for mydata in dataset:
        if mydata.id == request.user.id:
            names.append({'name':mydata.first_name+ ' '+ mydata.last_name+' (You) ' , 'y':mydata.TotalExpense , 'color':'#53F48D'})
        else:
            names.append({'name':mydata.first_name+ ' '+mydata.last_name , 'y':mydata.TotalExpense})

    print(names)
    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Spending Leaderboards'},
        'series': [{
        'name': 'Total Amount',
        'data': names,
        }]
    }

    return JsonResponse(chart)

def line_chart_leaderboard(request):

    # time=request.GET.get('time')
    # mydate=request.GET.get('mydate')
    # mydate1=request.GET.get('mydate1')
    # #lastconnection = datetime.strptime(mydate, '%d/%m/%Y').strftime('%Y-%m-%d')
   
    # ddate=parse_date(mydate)
    # theyear = ddate.year
    # theday = ddate.day
    # themonth = ddate.month

    # ddate1=parse_date(mydate1)
    # theyear1 = ddate1.year
    # theday1 = ddate1.day
    # themonth1 = ddate1.month

    # first_date = datetime.date(theyear, themonth, theday)
    # last_date = datetime.date(theyear1, themonth1, theday1)

    UserID=request.user.id
    # if time=='All':
    #     dataset = Expenses.objects.values('Date_Time__date').annotate(totalExpense=Sum('Amount')).filter(User_ID_id=UserID)
    # else:
    dataset =  Expenses.objects.raw('''SELECT "expense_expenses"."User_ID_id","auth_user"."id","auth_user"."first_name", "auth_user"."last_name", SUM("expense_expenses"."Amount") AS "TotalExpense" FROM "expense_expenses" INNER JOIN "Friends_friend" ON ("expense_expenses"."User_ID_id"="Friends_friend"."FriendID_id") INNER JOIN auth_user ON  ("expense_expenses"."User_ID_id"="auth_user"."id") WHERE "Friends_friend"."UserID_id"=%s GROUP BY "expense_expenses"."User_ID_id","auth_user"."id" ORDER BY "TotalExpense" DESC''',[UserID])

    names = list()
    totalExpense=list()


    for mydata in dataset:
        if mydata.id==request.user.id:
            names.append(mydata.first_name + ' '+ mydata.last_name+ " (You)" )
            totalExpense.append({"y":mydata.TotalExpense, "color":"#53F48D"})    
        else:
            names.append(mydata.first_name + ' '+ mydata.last_name )
            totalExpense.append({"y":mydata.TotalExpense , "color":"#8E44AD"} )    

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Spending Leader Boards'},
        'xAxis': {'categories': names},
        'series': [{
            'name': 'Total Amount',
            'data': totalExpense
        }]
    }

    return JsonResponse(chart)


def line_chart_insight(request):

    UserID=request.user.id
    dataset = Expenses.objects.values('Date_Time__date').annotate(totalExpense=Sum('Amount')).order_by('Date_Time__date')

    # names = list()
    # totalExpense=list()

    # for mydata in dataset:
    #     if mydata.id==request.user.id:
    #         names.append(mydata.first_name + ' '+ mydata.last_name+ " (You)" )
    #         totalExpense.append({"y":mydata.TotalExpense, "color":"#53F48D"})    
    #     else:
    #         names.append(mydata.first_name + ' '+ mydata.last_name )
    #         totalExpense.append({"y":mydata.TotalExpense , "color":"#8E44AD"} )    


    categories = list()
    totalExpense=list()

    for mydata in dataset:
        categories.append(mydata['Date_Time__date'])
        totalExpense.append({"y":mydata['totalExpense'] , "color":"#8E44AD"}) 

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Datewise Spendings'},
        'xAxis': {'categories': categories},
        'series': [{
            'name': 'Total Amount',
            'data': totalExpense
        }]
    }

    return JsonResponse(chart)

def pie_chart_insight(request):
 
    UserID=request.user.id

    dataset = Expenses.objects.values('Catagory').annotate(totalExpense=Sum('Amount')).order_by('-totalExpense')

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Catagory Distribution'},
        'series': [{
        'name': 'Total Amount',
        'data': list(map(lambda row: {'name': row['Catagory'], 'y': row['totalExpense']}, dataset))        }]
    }

    return JsonResponse(chart)