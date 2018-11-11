from django.shortcuts import render
from nokia import NokiaAuth, NokiaApi
import requests
import time
from samurai.settings import CLIENT_ID, CONSUMER_SECRET, CALLBACK_URI, CALLBACK_URI_TEST
from django.contrib.auth.models import User
from .models import Member, Group
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def test(request):
    # TODO: Test is on
    auth = NokiaAuth(CLIENT_ID, CONSUMER_SECRET, callback_uri=CALLBACK_URI_TEST)
    authorize_url = auth.get_authorize_url()
    return render(request, 'test.html', {"auth_url": authorize_url})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        u = User.objects.create(username=username)
        email = request.POST['email']
        password = request.POST['password']
        u.set_password(password)
        u.save()
        # TODO: Change time created to when the group was created
        time_created = int(time.time())
        new_member = Member(user=u, email=email, start_date=time_created)
        new_member.save()
        return HttpResponseRedirect('test/login/')
    return render(request, 'register.html')


def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/test/home')
    # TODO: Return error of user not found
    return render(request, 'login.html')


def success(request):
    if request.user.member.access_token is None:
        auth = NokiaAuth(CLIENT_ID, CONSUMER_SECRET, callback_uri=CALLBACK_URI_TEST)
        authorization_response = request.GET['code']
        credentials = auth.get_credentials(authorization_response)
        client = NokiaApi(credentials)
        request.user.member.update_credentials(credentials)
    weights = request.user.member.get_weights()
    days = request.user.member.get_days()
    return render(request, 'success.html', {'measures': weights, 'labels': days, 'measures2': [55, 56], 'name': "Pablo", 'name2': "Maria"} )


@login_required()
def home(request):
    if request.user.member.access_token is None:
        auth = NokiaAuth(CLIENT_ID, CONSUMER_SECRET, callback_uri=CALLBACK_URI_TEST)
        authorize_url = auth.get_authorize_url()
        return render(request, 'home.html', {"url": authorize_url})
    return HttpResponseRedirect('/test/success')


def test_success(request):
    auth = NokiaAuth(CLIENT_ID, CONSUMER_SECRET, callback_uri=CALLBACK_URI_TEST)
    authorization_response = request.GET['code']
    credentials = auth.get_credentials(authorization_response)
    client = NokiaApi(credentials)
    access_token = credentials.access_token
    meas_type = "6"
    category = "1"
    start_date = int(time.time())
    link = "https://wbsapi.withings.net/measure?action=getmeas&access_token=" + access_token + "&meastype=1&category=1"
    resp = requests.get(link)
    measures = client.get_measures()
    res = resp.json()['body']['measuregrps']
    weights, days = get_weights(res)
    return render(request, 'success.html', {'measures': weights, 'labels': days, 'measures2': [55, 54, 57, 54], 'name': "Pablo", 'name2': "Maria"})


def get_weights(json_res):
    weights_array = []
    labels_array = []
    for res in json_res:
        weight = res['measures'][0]['value']
        date = res['date']
        readable = time.ctime(date)
        labels_array.append(readable[0:11])
        real_weight = weight / 100
        weights_array.append(real_weight)
    return list(reversed(weights_array)), list(reversed(labels_array))
