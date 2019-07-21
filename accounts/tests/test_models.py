from django.test import TestCase
from accounts.models import CustomManager, PasswordHint

class TestPasswordHint(TestCase):

    def setUp(self):
        self.firstuser = PasswordHint.objects.create(
            username='user1',
            hint='my hint',
            email='user1@gmail.com',
        )

    def test_hint_assigned_to_user(self):
        self.assertEquals(self.firstuser.hint, 'my hint')

    # def test_default_hint(self):
    #     self.seconduser = PasswordHint.objects.create(
    #         username='user1',
    #         hint='',
    #         email='user1@gmail.com',
    #     )

    #     self.assertEquals(self.seconduser.hint, 'No hint available')  