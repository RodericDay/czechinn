import urllib, datetime, copy

from django.core.urlresolvers import reverse, resolve
from django.shortcuts import render, redirect
from django.http import Http404

from czechinn.models import *
from czechinn.forms import *
from czechinn.adapter import *


def home(request):
    return render(request, 'home.html')

def profile(request):
    get_query = {
        'response_type': 'code',
        'redirect_uri': APP_URL + reverse('oauth_endpoint'),
        'client_id': CLIENT_ID,
    }
    context = {
        'auth_url': AUTH_BASE + '?' + urllib.parse.urlencode(get_query, doseq=True),
    }
    return render(request, 'registration/profile.html', context)

def oauth_endpoint(request):
    code = request.GET.get('code')
    if code:
        data = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': APP_URL + reverse('oauth_endpoint'),
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
        response = requests.post('https://drchrono.com/o/token/', data=data)
        response.raise_for_status()
        access_token = response.json().get('access_token')

        profile, new = Profile.objects.get_or_create(user=request.user)
        profile.access_token = access_token
        profile.save()

    return redirect('profile')

def json_table(request):
    extra = {'date': datetime.date.today()}
    context = adapter(request, 'get', request.GET['q'], extra)
    return render(request, 'json_table.html', context)

def new_patient(request):
    form = PatientForm(request.POST or None)
    context = {'form': form}

    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            patient = adapter(request, 'post', 'patients', data)
            return redirect('new-appointment', patient['id'])

    return render(request, 'actions/new_patient.html', context)

def transactional(request, patient_id=None):
    ''' very ephemeral login for patient '''
    form = TransactionForm(request.POST or None)
    context = {'form': form}

    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            first, sep, last = data['name'].partition(' ')
            extra = {
                'first_name': first,
                'last_name': last,
                'date_of_birth': data['date_of_birth'],
            }
            try:
                patient = adapter(request, 'get', 'patients_summary', extra)['results'][0]
                return redirect(request.GET['next'], patient['id'])
            except:
                raise Http404("No patient found matching those credentials")

    return render(request, 'actions/transactional.html', context)

def update_information(request, patient_id):
    current = adapter(request, 'get', 'patients_summary/'+patient_id)
    form = PatientForm(request.POST or current)
    context = {'form': form}

    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            adapter(request, 'put', 'patients_summary/'+patient_id, data)
            return redirect('update-information', patient_id)

    return render(request, 'actions/update_information.html', context)

def check_in(request, patient_id):
    # use next appointment from patients resource instead?
    extra = {'date': datetime.date.today(), 'patient': patient_id}
    try:
        appointment = adapter(request, 'get', 'appointments', extra)['results'][0]
    except IndexError:
        raise Http404("No appointments today")

    # unfurl datetime purely for display??
    dt, fmt = appointment['scheduled_time'], "%Y-%m-%dT%H:%M:%S"
    appointment['scheduled_time'] = datetime.datetime.strptime(dt, fmt)

    form = AppointmentForm(appointment)
    context = {'form': form}

    if request.method == "POST":
        data = form.data
        data['status'] = "Cancelled" if 'cancel' in request.POST else "Arrived"
        adapter(request, 'put', 'appointments/'+appointment['id'], form.data)
        return redirect('check-in', patient_id)

    return render(request, 'actions/check_in.html', context)

def new_appointment(request, patient_id):
    form = AppointmentForm(request.POST or None)
    context = {'form': form}

    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            data['patient'] = patient_id
            try:
                adapter(request, 'post', 'appointments', data)
                return redirect('check-in', patient_id)
            except Exception as err:
                if '409' in str(err):
                    form.add_error('scheduled_time', 'Timeslot not available')
                else:
                    form.add_error('scheduled_time', 'Mystery error!')

    return render(request, 'actions/new_appointment.html', context)

def schedule(request):
    extra = {'date': datetime.date.today()}
    context = adapter(request, 'get', 'appointments', extra)
    return render(request, 'schedule.html', context)
