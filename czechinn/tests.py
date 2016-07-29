import vcr
import requests

from django.test import TestCase


class TestSuite(TestCase):

    @vcr.use_cassette('cache/appointments.yml')
    def test_one(self):
        response = requests.get('https://google.com')
        response.raise_for_status()
