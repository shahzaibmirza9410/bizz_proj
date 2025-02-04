from django import forms
from django.contrib.auth.forms import UserCreationForm
from tempus_dominus.widgets import DatePicker
from bizz.models import User, Config,Script
from tempus_dominus.widgets import DateTimePicker

class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = '__all__'

status_choices = [
    ('pending', 'Pending'),
    ('failed', 'Failed'),
    ('in-progress', 'In Progress'),
    ('running', 'Running'),
]

schduled_choices = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('once', 'Once'),
]
days_choices = [
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thur', 'Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
    ('sun', 'Sunday'),
]
active_choices = [
    ('False', 'False'),
    ('True', 'True'),

]

class ScriptsForm(forms.ModelForm):
    short_description = forms.CharField(max_length=400, required=False)
    schedule_frequency = forms.ChoiceField(choices=schduled_choices, required=False)
    schedule_day = forms.ChoiceField(choices=days_choices, required=False)
    schedule_active = forms.ChoiceField(widget=forms.RadioSelect,choices=active_choices, required=False)
    schedule_once = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),required=False
    )
    monthly_dates = forms.CharField(max_length=400, required=False,widget=forms.TextInput(attrs={'placeholder': 'Comma separated dates i.e. 1,12,24, etc'}))

    class Meta:
        model = Script
        fields = (
            'title', 'short_description', 'schedule_frequency','schedule_active','schedule_day','schedule_once','monthly_dates')
