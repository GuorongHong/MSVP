from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class SignUpForm(UserCreationForm):
    hint = forms.CharField(
        label='(Optional) Password Hint', 
        max_length=200, 
        help_text=mark_safe('The hint shown if you forget your password. <br /> Do not edit if you do not wish to include a hint. <br /> You may add and edit hints after you log in.'), 
        # widget=forms.TextInput(attrs={"placeholder":""}),
        required=False,
        # initial="No hint available",
        )
    
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'hint')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.hint = self.cleaned_data['hint']
        user.email = self.cleaned_data['email']

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

    email = forms.EmailField(
        max_length=254,
        help_text='Confirm your email address.',
        widget=forms.TextInput(attrs={"placeholder":"Your email"})
    )

    def username_present(crsf, username):
        if User.objects.filter(username=username).exists():
            return username
            
        return False

    def email_confirm(crsf, username, email):
        if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():
            return True
        
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

class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={"placeholder":"New email here"}),)

    def __str__(self):
        return self.new_email