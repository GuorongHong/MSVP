from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    hint = forms.CharField(
        label='(Optional) Password Hint', 
        max_length=200, 
        help_text='The hint shown if you forget your password.', 
        required=False,
        )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'hint')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = cleaned_data['username']
        user.hint = cleaned_data['hint']

        if commit:
            user.save()

        return user

class GetHintForm(forms.Form):
    username = forms.CharField(
        label="Username", 
        max_length=200, 
        help_text='Input username to retrieve hint for master password.',
        widget=forms.TextInput(attrs={"placeholder":"Your username"})
        )

    def username_present(crsf, username):
        if User.objects.filter(username=username).exists():
            return username
            
        return False
