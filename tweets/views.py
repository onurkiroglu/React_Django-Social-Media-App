
import random
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .forms import TweetForm
from .models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    print('post data is', request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.save()
        form = TweetForm()
    return render(request, 'components/form.html', context={"form":form})

def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    """
    qs = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content":x.content, "likes":random.randint(0, 150)} for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view(response, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    """
    
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id = tweet_id)
        data['content'] = obj.content
        
    except: 
        data['message'] = "Not found"
        status = 404
    
    return JsonResponse(data, status=status)