from django.test import TestCase
from password.models import Passwords

# class TestPasswords(TestCase):

#     def test_delete_user_cascade(self):
#         self.user1 = Passwords.objects.create(
#             user='user1',
#             userid='user1',
#             pw='password',
#             web='www.user1.com',
#             email='user1@gmail.com',
#         )

#         self.user1.save()
#         self.user1.user.delete()
#         self.assertFalse(self.user1.pw.exists())