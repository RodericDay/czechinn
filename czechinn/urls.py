import requests

from django.conf.urls import url, include
from django.contrib.auth.views import login, logout

from czechinn.views import *


urlpatterns = [
    url(r'^$', home, name="home"),

    url(r'^login/$', login, name="login"),
    url(r'^logout/$', logout, name="logout"),

    url(r'^o/$', oauth_endpoint, name="oauth_endpoint"),

    url(r'^profile/$', profile, name="profile"),
    url(r'^q/$', json_table, name="json-table"),  # utility view

    url(r'^new-patient/$', new_patient, name="new-patient"),
    url(r'^transactional/$', transactional, name="transactional"),
    url(r'^update-information/(\d{8})/$', update_information, name="update-information"),
    url(r'^new-appointment/(\d{8})/$', new_appointment, name="new-appointment"),
    url(r'^check-in/(\d{8})/$', check_in, name="check-in"),

    url(r'^schedule/', schedule, name="schedule"),
]
