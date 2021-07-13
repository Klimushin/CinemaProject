from cinema.models import Session, Ticket
from django import forms
from django.utils.translation import gettext as _


class CreateSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('hall', 'start_time', 'end_time', 'start_date', 'end_date', 'price')
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hall = cleaned_data['hall']
        start_time = cleaned_data['start_time']
        end_time = cleaned_data['end_time']
        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']
        if start_time > end_time or start_date > end_date:
            self.add_error('start_time', _('The start time cannot be greater than the end'))

        sessions_that_overlap = hall.sessions.filter(status=True, end_date__gte=start_date, start_date__lte=end_date)
        if sessions_that_overlap:
            if sessions_that_overlap.filter(end_time__gte=start_time, start_time__lte=end_time):
                self.add_error('hall', _('The hall is busy at this time'))


class TicketForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = Ticket
        fields = ('quantity',)


class FilterForm(forms.Form):
    filter_price = forms.BooleanField(label=_('Filter by price'), required=False)
    filter_start_time = forms.BooleanField(label=_('Filter by start'), required=False)
