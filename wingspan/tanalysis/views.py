from django.shortcuts import render

# Create your views here.
<<<<<<< Updated upstream
=======
def index(request):
    """
    For the time being, the view just renders a list of tweets from a random keyword.
    This is where the frontend is rendered.
    """
    try:
        twitter_launcher = TwitterCom()
        tweets = twitter_launcher.search_tweets("bachelorette", 20)
    except:
        tweets = []
    html = "<html><body> %s </body></html>" % tweets
    return HttpResponse(html)
>>>>>>> Stashed changes
