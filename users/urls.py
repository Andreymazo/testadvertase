                                                                 
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from users.apps import UsersConfig
from users.views import log_out, log_in, my_registration, users_lst
app_name = UsersConfig.name

urlpatterns = [

    path('', log_in, name='log_in'),
        #   CustomLoginView.as_view(template_name='registration/login.html')
    path('log_out', log_out, name='log_out'),
    path('my_registration', my_registration, name='my_registration'),
    path('users_lst', users_lst, name='users_lst'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
