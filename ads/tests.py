from django.test import TestCase
from django.urls import reverse

from ads.form import CreateAdsForm
from users.forms import MyRegForm
from users.models import CustomUser


"""Команда python manage.py test"""
class CreateUserAdsFormTest(TestCase):
    
    def setUp(self): 
        self.user = CustomUser.objects.create(email="andreymazo3@mail.ru")

    """ Здесь 'password1' не равен 'password2'"""
    def test_MyRegForm_valid_passw(self):
        form = MyRegForm(data={'password1': "rrr", 'password2': self.user.id, 'email': "op@yuik.com",})
        self.assertFalse(form.is_valid())

    """ Здесь 'email' не valid"""
    def test_MyRegForm_valid_email(self):
        form = MyRegForm(data={'password1': "rrr", 'password2': "rrr", 'email': "op",})
        self.assertFalse(form.is_valid())

    def test_MyRegForm_invalid(self):
        form = MyRegForm(data={'password1': "rrr", 'password2': "rrr", 'email': "op@yuik.com",})
        self.assertTrue(form.is_valid())

    """ Здесь 'user': self.user.id  """
    def test_Ads_valid(self):
        form = CreateAdsForm(data={'title': "rrr", 'user': self.user.id, 'category': "op", 'description': 'fff',\
                                    'image':'media/Screenshot_from_2025-05-11_00-09-20.png' , 'status':'STATUS_NEW'})
        self.assertTrue(form.is_valid())

    """ Здесь 'user': "mp" """
    def test_Ads_invalid(self):
        form = CreateAdsForm(data={'title': "tt", 'user': "mp", 'category': "mp", 'description': "fff", \
                                   'image':'', 'status':'STATUS_NEW'})
        self.assertFalse(form.is_valid())
        

