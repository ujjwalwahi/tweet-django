from .forms import StatusForm
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import render
import tweepy
import requests.packages.urllib3
from django.http import HttpResponse
from urlparse import urlparse, parse_qs
from django.shortcuts import redirect
requests.packages.urllib3.disable_warnings()


def twitterAuthenticate(request):    
    oauth_verifier =  request.GET.get('oauth_verifier', None)    
    consumer_key = 'u2q9wRYm39FNfO5pRAW5TRC5I'
    consumer_secret = '3laxjeOWk95UjI3bkjR6PIWLJZI6J1KyetIV2z0BvUDJ8xfqq3'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    if oauth_verifier:        
        # session['request_token'] = auth.request_token        

        # # request.session['request_token'] = (auth.request_token.key, auth.request_token.secret)
        # # verifier = request.GET.get('oauth_verifier')

        # # auth = tweepy.OAuthHandler('consumer_token', 'consumer_secret,''callback_url')

        # # token = request.session.get('request_token')
        # # request.session.delete('request_token')
        # # # auth.set_request_token(token[0], token[1])
        # # auth.request_token = session.get('request_token')

        # query_params = parse_qs(urlparse(redirect_url).query)
        # oauth_token = query_params['oauth_token'][0]
        
        # verifier = redirect_url
        try:
            verifier = request.GET.get('oauth_verifier')            
            token = request.GET.get('oauth_token')            
            #auth.request_token = token
            try:
                auth.set_access_token(token, verifier)
                response = 'authenticate success'
            except tweepy.TweepError as e:
                print 'Error! Failed to get access token.'           
                print(e)
                response = 'Error! Failed to get access token.'
            # response_data = {}
            # response_data['key'] = auth.access_token.key
            # response_data['secret'] = auth.access_token.secret
            # response = 'you are now authenticated'
            # api = tweepy.API(auth)
            # api.update_status('tweepy + oauth!')
        except Exception as e:
            print "TweepError"    
            print(e)
            response = 'authenticate error '
    else:        
        access_token = ''
        access_token_secret= ''
        session = {}
        callback_url = 'http://localhost:8000'
        response = 'Success! Failed to get request token.'        
        try:        
            redirect_url = auth.get_authorization_url()    
            access_token = parse_qs(urlparse(redirect_url).query)['oauth_token'][0]
            print("session set")
            print(access_token)
            request.session['request_token'] = access_token            
            print(request.session.get('request_token', 'Nothing'))
            return redirect(redirect_url)            
        except tweepy.TweepError:
            response = 'Error! Failed to get request token.'            
    return HttpResponse(response)


def twitterAuthorizeCallback(request):
    verifier = request.GET.get('oauth_verifier')

    auth = tweepy.OAuthHandler('consumer_token', 'consumer_secret')

    token = request.session.get('request_token')
    request.session.delete('request_token')
    auth.set_request_token(token[0], token[1])

    try:
        token = auth.get_access_token(verifier)
    except tweepy.TweepError:
        return HttpResponse('error', status=500)

    # response_data = {}
    # response_data['key'] = auth.access_token.key
    # response_data['secret'] = auth.access_token.secret
    session ={}
    session['token'] = (auth.access_token, auth.access_token_secret)
    # auth.set_access_token(access_token, access_token_secret)
    token, token_secret = session['token']
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(token, token_secret)

    response = 'you are now authenticated'
    api = tweepy.API(auth)
    api.update_status('tweepy + oauth!')
    return HttpResponse(response)



