from django import forms

class SlotForm(forms.Form):
    start_time = forms.DateTimeField(required=True)
    end_time = forms.DateTimeField(required=True)

class SubjectUploadForm(forms.Form):
    file = forms.FileField()