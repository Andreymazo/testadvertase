from django.test import TestCase, Client
from django.urls import reverse
from ads.form import CreateAdsForm
from ads.models import Advertisement
from users.forms import MyRegForm
from users.models import CustomUser
from django.utils import timezone 

from django.contrib.auth import get_user_model

"""How to use fixtures?"""
# @pytest.fixture
# def setup_data_ads():  
#     user = CustomUser.objects.create(email="andreyzo3@mail.ru")
#     data = Advertisement(
#         category = "tds",user = user, title = 'asddd', description = 'ppp', \
#         image = '/home/andreymazo/Pictures/Screenshots/Screenshot from 2025-03-10 12-11-04.png',\
#         created = timezone.now(), status = 'STATUS_USED') 
#     return data  
User = get_user_model()
"""Команда python manage.py test"""
class CreateUserAdsFormTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='reg@reg.reg', password='reg')
        self.user2 = User.objects.create_user(email='reg@reg2.reg', password='reg2')
        self.path_ads_lst = reverse('ads:ads_lst')
        self.url_reg = reverse('users:my_registration')
        self.data_reg = {'email':'reg@reg.reg', 'password1':'reg', 'password2':'reg'}
        self.url_log = reverse('users:log_in')
   
        
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


    """ Здесь ok """
    def test_Ads_valid(self):
        form = CreateAdsForm(data={'title': "rrr", 'user':self.user, 'category': "op", 'description': 'fff',\
                                    'image':'media/Screenshot_from_2025-05-11_00-09-20.png' , 'status':'STATUS_NEW'})
        self.assertTrue(form.is_valid())


    """ Здесь 'title': None """
    def test_Ads_invalid(self):
        form = CreateAdsForm(data={'title': None, \
                                   'category': "mp", 'description': "fff", \
                                   'image':'', 'status':'STATUS_NEW'})
        self.assertFalse(form.is_valid())


    """Проверка авторизации"""
    def test_auth(self):
        data = {'email':self.data_reg['email'], 'password':self.data_reg['password1']}
        response1 = self.client.post(self.url_log, data=data)
        self.assertTrue(response1.status_code,200)
       

    """Проверка гет заппроса на список объявленирй"""
    def test_list_ads(self):
        response = self.client.get(self.path_ads_lst)
        self.assertTrue(response.status_code, 200)

# https://www.geeksforgeeks.org/how-to-authenticate-a-user-in-tests-in-django/
    """Создаем объявление.Перед созданием авторизироваться"""
    def test_create_ads(self):
        data_ads =  {'category': "tds", 'user': self.user, 'title': 'asddd', 'description': 'ppp', \
        'image': '/home/andreymazo/Pictures/Screenshots/Screenshot from 2025-03-10 12-11-04.png',\
        'created':  timezone.now(), 'status' :'STATUS_USED'}
        self.client.login(email='reg@reg.reg', password='reg')
        response = self.client.post(self.path_ads_lst,data=data_ads )
        self.assertEqual(Advertisement.objects.count(), 1)
        ads = Advertisement.objects.first()
        self.assertRedirects(response, reverse('ads:create_ads_confirm', args=[ads.id]))


    """Изменяем объявление"""
    def test_update_ads(self):
        self.client.login(email='reg@reg.reg', password='reg')
        data = {'category': "tdsss", 'user': self.user, 'title': 'asddd', 'description': 'ppp', \
        'image': '/home/andreymazo/Pictures/Screenshots/Screenshot from 2025-03-10 12-11-04.png',\
        'created':  timezone.now(), 'status' :'STATUS_USED'}
        ads = Advertisement.objects.create(**data)
        response = self.client.post(
            reverse('ads:update_ads_confirm', kwargs={'pk': ads.id}),
            {'category': "sss", 'user': self.user, 'title': 'asddd', 'description': 'ppp', \
        'image': '/home/andreymazo/Pictures/Screenshots/Screenshot from 2025-03-10 12-11-04.png',\
        'created':  timezone.now(), 'status' :'STATUS_USED'})
        self.assertEqual(response.status_code, 302)
        ads.refresh_from_db()
        self.assertEqual(ads.category, 'sss')
        self.assertRedirects(response, reverse('ads:create_ads_confirm', args=[ads.id]))
 

    """Удаляем объявление. Создаем сначала свое пост запросом. Переходим на delete_ads/<int:pk> и пост запросом удаляем это объявление"""
    def test_delete_ads(self):
        
        self.client.login(email='reg@reg.reg', password='reg')
        data = {'category': "tdsss", 'user': self.user, 'title': 'asddd', 'description': 'ppp', \
        'image': '/home/andreymazo/Pictures/Screenshots/Screenshot from 2025-03-10 12-11-04.png',\
        'created':  timezone.now(), 'status' :'STATUS_USED'}
        ads_instance=Advertisement.objects.create(**data)
        url_ads_delete=reverse('ads:delete_ads_confirm', kwargs={'pk': ads_instance.id})
        response1 = self.client.post(self.path_ads_lst,data=data )
        number1 = Advertisement.objects.count()
        response2 = self.client.post(url_ads_delete)
        self.assertRedirects(response2, reverse('ads:ads_lst'))
        number2 = Advertisement.objects.count()
        self.assertEqual(number1, number2-1)

    """Удаляем объявление. Создаем какое-то не свое. Все чтио в предыдущем, только не удалит. \
        на 1 больше и перенаправляет на эндпоинт - кастом ворнинг"""
    def test_delete_ads(self):
        
        self.client.login(email='reg@reg.reg', password='reg')
        data = {'category': "tdsss", 'user': self.user, 'title': 'asddd', 'description': 'ppp', \
        'image': '/home/andreymazo/Pictures/Screenshots/Screenshot from 2025-03-10 12-11-04.png',\
        'created':  timezone.now(), 'status' :'STATUS_USED'}
        ads_instance=Advertisement.objects.create(**data)
        url_ads_delete=reverse('ads:delete_ads_confirm', kwargs={'pk': ads_instance.id})
        response1 = self.client.post(self.path_ads_lst,data=data )
        self.client.login(email='reg@reg2.reg', password='reg2')
        number1 = Advertisement.objects.count()
        response2 = self.client.post(url_ads_delete)
        self.assertRedirects(response2, reverse('ads:custom_warning'))
        number2 = Advertisement.objects.count()
        self.assertEqual(number1, number2)

    # """Создаем предложение"""
    # def test_create_prop(self):
    #     data =
    #     self.assertTrue(data)

    # """Изменяем предложение"""
    # def test_update_ads(self):
    #     self.assertTrue(data)
    
    # """Удаляем предложение"""
    # def test_delete_prop(self):
    #     data =
    #     self.assertTrue(data)

