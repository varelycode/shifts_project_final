from django import forms
from django.contrib.auth import get_user_model

from .models import Run, Shift
import pdb

User = get_user_model()


class EmployeeForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=User.objects.all())


class ShiftForm(forms.ModelForm):
    start_datetime = forms.SplitDateTimeField(input_time_formats=['%I:%M %p'])
    end_datetime = forms.SplitDateTimeField(input_time_formats=['%I:%M %p'])

    class Meta:
        model = Shift
        fields = ('shifts_text', 'start_datetime', 'end_datetime')

    def clean(self):
        start = self.cleaned_data['start_datetime']
        end = self.cleaned_data['end_datetime']

        if start > end:
            raise forms.ValidationError('The ending date must exceed the '
                                        'beginning date.')


class RunForm(forms.ModelForm):
    runs_start = forms.SplitDateTimeField(input_time_formats=['%I:%M %p'])
    runs_end = forms.SplitDateTimeField(input_time_formats=['%I:%M %p'])
    employees = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    class Meta:
        model = Run
        fields = ('runs_text', 'runs_start', 'runs_end', 'employees')

    def __init__(self, *args, **kwargs):
        self.shift = kwargs.pop('shift', None)
        super(RunForm, self).__init__(*args, **kwargs)

    def clean(self):
        first_run_tmp = "First run on Shift must start at the same time as the shift."
        run_start_before = "Run cannot start before shift."
        run_end_after = "Run cannot end after shift ends."
        start = self.cleaned_data['runs_start']
        end = self.cleaned_data['runs_end']

        if self.shift:
            shift_start = self.shift.start_datetime
            shift_end = self.shift.end_datetime

            # Tests if this is the first Run
            if not self.shift.get_runs_count():
                if not shift_start == start:
                    raise forms.ValidationError(first_run_tmp)

            # Test if run start/end times within shift start/end times
            if not start >= shift_start:
                raise forms.ValidationError(run_start_before)

            if not end <= shift_end:
                raise forms.ValidationError(run_end_after)

        # Test that Run Starts before it Ends
        if start > end:
            raise forms.ValidationError('The ending date must exceed the '
                                        'beginning date.')
