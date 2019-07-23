# from django.test import TestCase, Client
# from django.urls import reverse
# from accounts.models import PasswordHint, CustomManager
# from django.contrib.auth.models import User
# from django.utils.crypto import pbkdf2
# from unittest import skip

# class TestSignup(TestCase):

#     @skip
#     def setKey(self):
#         _, _, salt, _ = self.client.request.user.password.split('$')
#         key = pbkdf2(request.POST.get("Password"), salt, 50000, 48)
#         self.client.request.session['iv'] = key[0:16].hex()
#         self.client.request.session['cipherKey'] = key[16:].hex()

#     @skip
#     def login(self):
#         self.client.login(username='testuser', password='test')

#     def setUp(self):
#         self.client = Client()
#         self.url = reverse('signup')
#         self.template = 'signup.html'
#         self.verify = 'password/templates/password/verify_pw.html'
#         self.login = 'two_factor/core/login.html'

#         user = User.objects.create(username='testuser')
#         user.set_password('test')
#         user.save()

#     def testGET(self):
#         response = self.client.get(self.url, follow=True)

#         self.assertIn(response.status_code, [200, 302])
#         self.assertTemplateUsed(response, self.template)

# class TestLoginHint(TestSignup):

#     def setUp(self):
#         super().setUp()
#         self.url = reverse('login_hint')
#         self.template = 'login_hint.html'

# class TestAddHint(TestSignup):

#     def setUp(self):
#         super().setUp()
#         self.url = reverse('add_hint')
#         self.template = 'add_hint.html'

#     def testGET(self):
#         response = self.client.get(self.url, follow=True)

#         self.assertIn(response.status_code, [200, 302])
#         self.assertTemplateUsed(response, self.login)

#     def testGET_loggedIn(self):
#         super().login()
#         response = self.client.get(self.url, follow=True)

#         self.assertIn(response.status_code, [200, 302])
#         self.assertTemplateUsed(response, self.verify)

#     def testGET_verified(self):
#         super().setKey()
#         response = self.client.get(self.url, follow=True)

#         self.assertIn(response.status_code, [200, 302])
#         self.assertTemplateUsed(response, self.template)

# class TestChangeEmail(TestAddHint):

#     def setUp(self):
#         super().setUp()
#         self.url = reverse('change_email')
#         self.template = 'change_email.html'