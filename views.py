from site import makepath
from django.db import connection
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth

from examapp.models import Quetion
from loginapp.models import MyUser
# Create your views here.


def login(request):
    if request.method=='GET':

        return render(request,'loginapp/login.html')
    else:
        userobject=auth.authenticate(request,username=request.POST["username"],password=request.POST["password"])

        
        if(userobject.username!='admin'):

            print(connection.queries)

            print(userobject)

            username=userobject.username

            print(userobject.id)

            myuser=MyUser.objects.filter(user_ptr_id=userobject.id)

            imagepath=myuser[0].imagepath
            request.session["imagepath"]=imagepath

            print(myuser[0].imagepath)


        if userobject==None:
            return render(request,'loginapp/login.html',{"message":"credential are not correct"})
        else:
            auth.login(request,userobject)

            queryset=Quetion.objects.all().values('subject').distinct()

            print(f"subjects from db are :- {queryset}" )
            print(connection.queries)
            
            request.session["username"]=userobject.username
            request.session["score"]=0
            request.session["qindex"]=0
            request.session["answers"]={}
            request.session["duration"]=180

            if userobject.is_superuser==0:
                
                return render(request,'examapp/subject.html',{'listofdictionary':queryset, 'imagepath':imagepath, 'username':username}) 
            
            else:
                return render(request,'examapp/admindashboard.html')



def saveUser(request):
    if request.method=='GET':
        return render(request,'loginapp/register.html')
    
    
    photo=request.FILES['image']
    imagepath='/upload/'+photo.name

    with open('loginapp/static/upload/'+photo.name, 'wb+') as destination:  
                for byte in photo.chunks():  
                    destination.write(byte)

    MyUser.objects.create_user(username=request.POST["username"],email=request.POST["email"],password=request.POST["password"], imagepath=imagepath)
    
    #userobject.save()  # save the data in database table

    return render(request,'loginapp/login.html',{'message':'registration successful'})
   
