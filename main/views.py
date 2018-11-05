from django.shortcuts import render
from nokia import NokiaAuth, NokiaApi
import requests
import time
import mpld3

CLIENT_ID = "a2d850f43357b6fb2ab22a59b431ad3d438a0031d329ecec37686764e49b7939"
CONSUMER_SECRET = "7b52d21d03a644fe0491d7b0455a46264dfb7d055a36bb5be0ef7afc160c4bf1"
CALLBACK_URI_TEST = "http://127.0.0.1:8000/test/success"
CALLBACK_URI = "http://www.samuray.ml/test/success"


def test(request):
    # TODO: Test is on
    auth = NokiaAuth(CLIENT_ID, CONSUMER_SECRET, callback_uri=CALLBACK_URI_TEST)
    authorize_url = auth.get_authorize_url()
    return render(request, 'test.html', {"auth_url": authorize_url})


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
    return render(request, 'success.html', {'measures': weights, 'labels': days})


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
