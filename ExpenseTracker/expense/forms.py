from django import forms

class DateForm(forms.Form):
    my_date_field=forms.DateTimeField()