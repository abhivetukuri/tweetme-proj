import random
from telnetlib import STATUS
from django.conf import settings
from nturl2path import url2pathname
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


#from tweetme.settings import ALLOWED_HOSTS
from .models import Tweet
from .forms import TweetForm

#ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request,*args,**kwargs):
    #return HttpResponse("<h1>Hello World</h1>")
    return render(request,"pages/home.html",context={},status=200)

@api_view(['POST']) #HTTP method client must send is POST
#@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request,*args, **kwargs):
    serializer = TweetSerializer(data=request.POST or None)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['GET','DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet"}, status = 401)
    obj = qs.first()
    obj.delete()
    serializer = TweetSerializer(obj)
    return Response({"message": "Tweet removed"}, status=200)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs,many=True)
    return Response(serializer.data, status=200)

def tweet_create_view_pure_django(request,*args, **kwargs):
    ''' 
    REST API Create View (REST Framework)
    '''
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        #do other form related logic
        obj.user = user 
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), STATUS=201)
        if next_url != None: #and is_safe_url(next_url):
            return redirect(next_url)
        form = TweetForm()
    if form.error_class:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, "components/form.html", context ={"form": form})

def tweet_list_view_pure_django(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JS or Swift or Java
    return JSON data
    """
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs] 
    data = {
        "is_user": False,
        "response": tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JS or Swift or Java
    return JSON data
    """
    data = {"id": tweet_id,
        #"image_path": obj.image.url
        #"content": obj.content
    }
    
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404
    return JsonResponse(data, status=status) 
    #return HttpResponse(f"<h2>Hello {tweet_id} - {obj.content}</h2>")