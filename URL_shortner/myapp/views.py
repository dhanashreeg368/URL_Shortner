from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import LongtoShort

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello world!")

def home_page(request):
    context= {
        "submitted": False,
        "error": False
    }
    if request.method == 'POST':
        data=request.POST # dict
        # context["submitted"]= True
        # print(request.post)
        
        long_url = data['longurl']
        custom_name = data['custom_name']

        try:
            #create
            obj = LongtoShort(long_url = long_url, short_url = custom_name) #inserting in db
            obj.save()

            #read
            date = obj.date
            clicks = obj.clicks
            context["long_url"]=long_url
            context["short_url"]= request.build_absolute_uri() + custom_name
            context["date"] = date
            context["clicks"] = clicks                       
            context["submitted"] = True
        except:
            context["error"] = True
    else:
        print("User not sending anything")
    # print(request.method) to see request method use this
    return render(request, 'index.html', context) # to open page use renderr

def redirect_url(request, short_url):
    row = LongtoShort.objects.filter(short_url = short_url)
    if len(row) == 0:
        return HttpResponse("No such url exists")
    obj = row[0]
    long_url = obj.long_url

    obj.clicks = obj.clicks + 1
    obj.save()
    return redirect(long_url)

def all_analytics(request):
    rows = LongtoShort.objects.all()
    context = { 
        "rows": rows
    }
    return render(request, "all-analytics.html",context)

def task(request):
    # send dynamic data
    context = {
        "my_name": "Dhanashree", # to display dynamic name in html from here
        "x": "5"
    }
    return render(request, "test.html", context )
