from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.db.models import Q

# Create your views here.

def index(request):
    if request.user.is_authenticated:

        return render(request,"friends/index.html")
    else:
        return render('login')


def leaderboards(request):
    if request.user.is_authenticated:
        return render("friends/index.html")
    else:
        return render('login')

def search(request):
    if request.user.is_authenticated:
        search=request.GET['search']
        result = User.objects.all().filter(Q(first_name__icontains=search)|Q(last_name__icontains=search))
        

        context={
            "searchresults":result,
        }
        return render(request,"friends/search.html",context)
    else:
        return render('login')
    