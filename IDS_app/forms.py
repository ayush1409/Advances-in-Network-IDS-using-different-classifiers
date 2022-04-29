from django import forms

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50, required = True)
    log_file = forms.FileField(required = True)