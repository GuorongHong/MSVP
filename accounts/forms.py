from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class SignUpForm(UserCreationForm):
    hint = forms.CharField(
        label='(Optional) Password Hint', 
        max_length=200, 
        help_text=mark_safe('The hint shown if you forget your password. <br /> Do not edit if you do not wish to include a hint. <br /> You may add and edit hints after you log in.'), 
        widget=forms.TextInput(attrs={"placeholder":""}),
        initial="No hint available",
        )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'hint')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.hint = self.cleaned_data['hint']

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

class AddHintForm(forms.Form):
    new_hint = forms.CharField( 
        max_length=200, 
        ##help_text='Do not edit if you do not wish to include a hint.', 
        widget=forms.TextInput(attrs={"placeholder":"New hint here"}),
        required=False,
        )

    def __str__(self):
        return self.new_hint