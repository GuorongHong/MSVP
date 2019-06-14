from django import forms 

class PasswordForm(forms.Form):
    userid = forms.CharField(label='UserID', max_length = 200)
    pw = forms.CharField(label='Password', max_length = 200)
    web = forms.CharField(label='Website', max_length = 200)
