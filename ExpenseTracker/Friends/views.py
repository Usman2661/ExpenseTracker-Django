from django.shortcuts import render , redirect
from django.contrib.auth.models import User,auth
from django.db.models import Q
from django.contrib import messages
from Friends.models import Request,Friend

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        MyUserID=request.user.id
        myrequests = Request.objects.all().filter(SentTo=MyUserID)
        context={
            'requests':myrequests,
        }
        return render(request,"friends/index.html",context)
    else:
        return render('login')


def leaderboards(request):
    if request.user.is_authenticated:
        return render("friends/index.html")
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
            result = User.objects.all().filter(Q(first_name__icontains=search)|Q(last_name__icontains=search))
            context = {
                "searchresults":result,
            }
            return render(request,"friends/search.html",context)
    else:
        return render('login')
    