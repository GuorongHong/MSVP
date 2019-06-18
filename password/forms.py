from django import forms 

class PasswordForm(forms.Form):
    userid = forms.CharField(label='UserID', max_length = 200)
    pw = forms.CharField(label='Password', max_length = 200)
    web = forms.CharField(label='Website', max_length = 200)

class GeneratePasswordForm(forms.Form):
    length = forms.IntegerField(label='Length', min_value = 4, max_value = 128)
    use_upper = forms.BooleanField(label="Uppercase", initial = True, required = False)
    use_lower = forms.BooleanField(label="Lowercase", initial = True, required = False)
    use_digits = forms.BooleanField(label="Digits", initial = True, required = False)
    use_special = forms.BooleanField(label="Special characters", initial = True, required = False)
    avoid_similar = forms.BooleanField(label="Avoid similar letters and numbers", initial = True, required = False)
    
    def validation_message(self):
        length = self.clean_data.get('length', '')
        upper = self.clean_data.get('use_upper', '')
        lower = self.clean_data.get('use_lower', '')
        digits = self.clean_data.get('use_digits', '')
        special = self.clean_data.get('use_special', '')
        avoid_similar = self.clean_data.get('avoid_similar', '')

        if length or upper or lower or digits or special or avoid_similar:
             raise forms.ValidationError("Please select at least one.")