from django.test import TestCase
from password.forms import PasswordForm, GeneratePasswordForm

class TestPasswordForm(TestCase):

    def test_password_form_valid_data(self):
        form = PasswordForm(data={
            'web':'www.hello.com',
            'userid':'hello',
            'pw':'password',
            'email':'hello@gmail.com',
        })

        self.assertTrue(form.is_valid())
    
    def test_password_form_missing_data(self):
        form = PasswordForm(data={
            'web':'www.hello.com',
            'userid':'hello',
            'pw':'',
            'email':'',
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

class TestGeneratePasswordForm(TestCase):

    def test_generate_password_form_valid_data(self):
        form1 = GeneratePasswordForm(data={
            'length':12,
            'use_upper':True,
            'user_lower':False,
            'use_digits':True,
            'use_special':True,
            'avoid_special':True,
            'personal_details':'hello,bye'
        })

        # test when personal details is empty
        form2 = GeneratePasswordForm(data={
            'length':12,
            'use_upper':True,
            'user_lower':False,
            'use_digits':True,
            'use_special':True,
            'avoid_special':True,
            'personal_details':''
        })

        self.assertTrue(form1.is_valid()) 
        self.assertTrue(form2.is_valid())

    def test_generate_password_form_length_min(self):
        form = GeneratePasswordForm(data={
            'length':3,
            'use_upper':True,
            'user_lower':False,
            'use_digits':True,
            'use_special':True,
            'avoid_special':True,
            'personal_details':'hello,bye'
        })

        self.assertFalse(form.is_valid())        

