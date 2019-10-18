from django.shortcuts import render , redirect
from django.contrib.auth.models import User,auth
from django.db.models import Q
from django.contrib import messages
from Friends.models import Request,Friend

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        MyUserID=request.user.id
        #myrequests=User.objects.filter(UserID_SentTo=MyUserID)
        #myrequests = Request.objects.select_related('SentTo').filter(SentTo_id=MyUserID)
        #myrequests.SentTo_id.Username
       
        #myrequests = User.objects.filter(UserID_SentTo = MyUserID)
        myrequests = Request.objects.filter(SentTo=MyUserID)
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
            UserID=request.user.id
            result = User.objects.all().filter(Q(first_name__icontains=search)|Q(last_name__icontains=search)|(Q(username__icontains = search )))
            result=result.filter(~Q(id = UserID))
            context = {
                "searchresults":result,
            }
            return render(request,"friends/search.html",context)
    else:
        return render('login')
    