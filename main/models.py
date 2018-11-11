from django.db import models
from nokia import NokiaAuth, NokiaApi, NokiaCredentials
import requests
import time
from django.contrib.auth.models import User
from samurai.settings import CLIENT_ID, CONSUMER_SECRET


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    email = models.EmailField(max_length=150, null=True)
    access_token = models.TextField(null=True)
    token_expiry = models.TextField(null=True)
    token_type = models.TextField(null=True)
    refresh_token = models.TextField(null=True)
    api_id = models.TextField(null=True)
    start_date = models.IntegerField(default=0)

    # TODO: Make get_weights and get days into the same function that returns 2 arrays
    def get_weights(self):
        access_link = "https://account.withings.com/oauth2/token"
        headers = {'grant_type': 'refresh_token', 'client_id': CLIENT_ID, 'client_secret': CONSUMER_SECRET, 'refresh_token': str(self.refresh_token)}
        req = requests.post(access_link, data=headers)
        self.update_access_token(req.json())
        link = "https://wbsapi.withings.net/measure?action=getmeas&access_token=" + self.access_token + "&meastype=1&category=1&startdate=" + str(self.start_date) + "&enddate=" + str(int(time.time()))
        response = requests.get(link)
        response_in_json = response.json()['body']['measuregrps']
        return self.get_array_of_weights(response_in_json)

    def get_days(self):
        access_link = "https://account.withings.com/oauth2/token"
        headers = {'grant_type': 'refresh_token', 'client_id': CLIENT_ID, 'client_secret': CONSUMER_SECRET,
                   'refresh_token': str(self.refresh_token)}
        req = requests.post(access_link, data=headers)
        self.update_access_token(req.json())
        link = "https://wbsapi.withings.net/measure?action=getmeas&access_token=" + self.access_token + "&meastype=1&category=1&startdate=" + str(
            self.start_date) + "&enddate=" + str(int(time.time()))
        response = requests.get(link)
        response_in_json = response.json()['body']['measuregrps']
        return self.get_array_of_days(response_in_json)

    def get_array_of_weights(self, response):
        weights_array = []
        for res in response:
            weight = res['measures'][0]['value']
            real_weight = weight / 100
            weights_array.append(real_weight)
        return list(reversed(weights_array))

    def get_array_of_days(self, response):
        labels_array = []
        for res in response:
            date = res['date']
            readable = time.ctime(date)
            labels_array.append(readable[0:11])
        return list(reversed(labels_array))

    def update_credentials(self, credentials):
        self.access_token = credentials.access_token
        self.token_expiry = credentials.token_expiry
        self.token_type = credentials.token_type
        self.refresh_token = credentials.refresh_token
        self.api_id = credentials.user_id
        self.save()

    def update_access_token(self, credentials):
        self.access_token = credentials['access_token']
        self.token_expiry = credentials['expires_in']
        self.refresh_token = credentials['refresh_token']
        self.save()

    def __str__(self):
        return self.user.username


class Group(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    user1 = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='user1')
    user2 = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='user2')
    user3 = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='user3')
    user4 = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='user4')
    user5 = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='user5')

    def __str__(self):
        return self.unique_id
