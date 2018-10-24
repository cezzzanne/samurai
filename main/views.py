from django.shortcuts import render

CLIENT_ID = "a2d850f43357b6fb2ab22a59b431ad3d438a0031d329ecec37686764e49b7939"
CONSUMER_SECRET = "7b52d21d03a644fe0491d7b0455a46264dfb7d055a36bb5be0ef7afc160c4bf1"
CALLBACK_URI = "http://www.samuray.ml/test"


def test(request):
    # auth = NokiaAuth(CLIENT_ID, CONSUMER_SECRET, callback_uri=CALLBACK_URI)
    # authorize_url = auth.get_authorize_url()
    authorize_url = ""
    return render(request, 'test.html', {"auth_url": authorize_url})


