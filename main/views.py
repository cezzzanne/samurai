from django.shortcuts import render
from nokia import NokiaAuth, NokiaApi
CLIENT_ID = "a2d850f43357b6fb2ab22a59b431ad3d438a0031d329ecec37686764e49b7939"
CONSUMER_SECRET = "7b52d21d03a644fe0491d7b0455a46264dfb7d055a36bb5be0ef7afc160c4bf1"
CALLBACK_URI_TEST = "http://127.0.0.1:8000/test/success"
CALLBACK_URI = "http://www.samuray.ml/test/success"


def test(request):
    auth = NokiaAuth(CLIENT_ID, CONSUMER_SECRET, callback_uri=CALLBACK_URI)
    authorize_url = auth.get_authorize_url()
    return render(request, 'test.html', {"auth_url": authorize_url})


def test_success(request):
    auth = NokiaAuth(CLIENT_ID, CONSUMER_SECRET, callback_uri=CALLBACK_URI)
    authorization_response = request.GET['code']
    credentials = auth.get_credentials(authorization_response)
    client = NokiaApi(credentials)
    measures = client.get_measures(limit=1)
    return render(request, 'success.html', {'var': measures[0].weight})
