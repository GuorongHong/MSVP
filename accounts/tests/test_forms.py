from django.test import TestCase
from accounts.forms import SignUpForm, GetHintForm, AddHintForm, ChangeEmailForm
# from accounts.models import CustomManager, PasswordHint

class TestSignUpForm(TestCase):

    def test_signup_form_valid_data(self):
        form = SignUpForm(data={
            'username': 'hello',
            'email': 'hello@gmail.com', 
            'password1': 'SomeP@ssword2019', 
            'password2': 'SomeP@ssword2019', 
            'hint': 'my hint',
        })

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['hint'], 'my hint')

    def test_signup_form_no_data(self):
        form = SignUpForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
    
    def test_signup_form_diff_password(self):
        form = SignUpForm(data={
            'username': 'hello',
            'email': 'hello@gmail.com', 
            'password1': 'SomeP@ssword2019', 
            'password2': 'SomeOtherP@ssword2019', 
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_signup_form_invalid_email(self):
        form = SignUpForm(data={
            'username': 'hello',
            'email': 'hello', 
            'password1': 'SomeP@ssword2019', 
            'password2': 'SomeP@ssword2019', 
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

class TestGetHintForm(TestCase):

    def test_gethint_form_valid_data(self):
        form = GetHintForm(data={
            'username':'user1',
            'email':'user1@gmail.com'
        })

        self.assertTrue(form.is_valid())

class TestAddHintForm(TestCase):

    def test_addhint_form_valid_data(self):
        form = AddHintForm(data={
            'new_hint':'new hint',
        })

        self.assertTrue(form.is_valid())

    def test_addhint_form_no_data(self):
        form = AddHintForm(data={
            'new_hint':'',
        })

        self.assertTrue(form.is_valid())

class TestChangeEmailForm(TestCase):

    def test_changeemail_form_valid_data(self):
        form = ChangeEmailForm(data={
            'new_email':'newemail@gmail.com'
        })

        self.assertTrue(form.is_valid())

    def test_changeemail_form_no_data(self):
        form = ChangeEmailForm(data={
            'new_email':''
        })

        self.assertFalse(form.is_valid())

    def test_changeemail_form_invalid_email(self):
        form = ChangeEmailForm(data={
            'new_email':'newemail'
        })

        self.assertFalse(form.is_valid())