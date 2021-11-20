from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from tanalysis.models import Query, TwitterOutputData
from .twittercom import TwitterCom
from .sentiment import SentimentAnalyzer
import json

# Create your views here.

def index(request):
    """
    For the time being, the view just renders a list of tweets from a random keyword.
    This is where the frontend is rendered.
    """
    query = request.GET.get('query',None)
    if query is not None:
        sa = SentimentAnalyzer()
        tc = TwitterCom()
        tweets = tc.findTweets(query, 10)
        sa.analyzeTweets(tweets)
        tweets = list(map(lambda t: json.dumps(t), tweets))
        html = "<html><body> %s </body></html>" % tweets
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest()

def api(request):
    query_str = request.GET.get('query',None)
    users = request.GET.get('users', None)
    if query_str is not None:
        sa = SentimentAnalyzer()
        tc = TwitterCom()
        query = Query(query=query_str)
        tweets = tc.findTweets(query)
        scores = sa.analyzeTweets(tweets)
        top_tweets = tc.getTopTweets(tweets)
        output = json.dumps({"scores":scores, "top_tweets":top_tweets})
        return JsonResponse(output, safe=False)
    else:
        return HttpResponseBadRequest()
