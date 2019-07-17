from django import forms 
<<<<<<< HEAD
from django.utils.safestring import mark_safe
=======
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    hint = forms.CharField(label='Password Hint', max_length=200, help_text='(Optional) The hint shown if you forget your password', required=False, widget=forms.TextInput(attrs={"placeholder":"Password hint"}))

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
>>>>>>> custom_signup

class PasswordForm(forms.Form):
    web = forms.CharField(label='Website URL', max_length = 200, widget=forms.TextInput(attrs={"placeholder":"Website URL"}))
    userid = forms.CharField(label='UserID', max_length = 200, widget=forms.TextInput(attrs={"placeholder":"Your UserID"}))
    pw = forms.CharField(label='Password', max_length = 200, widget=forms.TextInput(attrs={"placeholder":"Your Password"}))
    email = forms.CharField(label='Email', max_length = 200, widget=forms.TextInput(attrs={"placeholder":"Your Email"}))
    
class GeneratePasswordForm(forms.Form):
    length = forms.IntegerField(label='Length', min_value = 4, max_value = 128)
    use_upper = forms.BooleanField(label="Uppercase", initial = True, required = False)
    use_lower = forms.BooleanField(label="Lowercase", initial = True, required = False)
    use_digits = forms.BooleanField(label="Digits", initial = True, required = False)
    use_special = forms.BooleanField(label="Special characters", initial = True, required = False)
    avoid_similar = forms.BooleanField(label="Avoid similar letters and numbers (Eg. 0 and O)", initial = True, required = False)
    personal_details = forms.CharField(
        label="(Optional) Personal Details", 
        help_text=mark_safe('Words or characters to be included in generated password. Separate each word with a comma and no spaces (eg. \"hello,bye\").'), 
        max_length = 200, 
        widget=forms.TextInput(attrs={"placeholder":"Details here"}),
        required = False)
    
    def clean(self):
        upper = self.cleaned_data['use_upper']
        lower = self.cleaned_data['use_lower']
        digits = self.cleaned_data['use_digits']
        special = self.cleaned_data['use_special']
        avoid_similar = self.cleaned_data['avoid_similar']
        personal_details = self.cleaned_data['personal_details']
        if upper == lower == digits == special == avoid_similar == False:
             raise forms.ValidationError("Please select at least one.")