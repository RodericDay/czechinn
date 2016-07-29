import datetime

from django import forms


DOCTORS = [(102522, 'Dr. Day')]

class TransactionForm(forms.Form):
    name = forms.CharField(initial="Sarah Chang")
    date_of_birth = forms.DateField(initial="1985-01-01")


class PatientForm(forms.Form):
    GENDER = [('Other', 'Other'), ('Male', 'Male'), ('Female', 'Female')]

    date_of_birth = forms.DateField()
    doctor = forms.ChoiceField(choices=DOCTORS)
    gender = forms.ChoiceField(choices=GENDER)
    first_name = forms.CharField()
    last_name = forms.CharField()


class AppointmentForm(forms.Form):
    # the patient field set by transactional
    doctor = forms.ChoiceField(choices=DOCTORS)
    duration = forms.ChoiceField(choices=[(15, '15m'), (30, '30m')])  # Duration field gives 00:00?
    exam_room = forms.ChoiceField(choices=[(1,'Red'), (2, 'Blue')])
    office = forms.ChoiceField(choices=[(109278, 'Rm1')])
    scheduled_time = forms.DateTimeField(initial=datetime.datetime.now)
    status = forms.CharField(required=False)
