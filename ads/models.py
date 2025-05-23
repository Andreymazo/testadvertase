from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

NULLABLE = {'blank': True, 'null': True}


STATUSES = [('STATUS_NEW', 'new'), ('STATUS_USED', 'used'),]

"""Модель - Объявленеие"""
class Advertisement(models.Model):
    
    category = models.CharField( max_length=150, verbose_name=_("Ads's category"))
    user = models.ForeignKey("users.CustomUser", related_name="user", on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name=_("Ads's title"))
    description = models.CharField(max_length=2000, verbose_name=_("Description"))
    image = models.ImageField(upload_to='media', **NULLABLE)
    created = models.DateTimeField(auto_now_add = True)
    status = models.CharField(choices=STATUSES, default='STATUS_USED')

    @property
    def image_url(self):
        if self.image :
            return self.image.url
        return ''

    def __str__(self):
        return str(self.title)
    

statut = [("waiting","waiting"), ("accepted","accepted"), ("rejected", "rejected"),]

"""Модель - Предложение"""
class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, \
                                  related_name='sender', verbose_name="Номер инициатора предложения")
    ad_receiver = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE,\
                                     related_name='receiver', verbose_name="Номер принимающего предложения")
    comment = models.CharField(max_length=350 , verbose_name="Комментраий")
    status = models.CharField(choices=statut, default="waiting")
    created_at =  models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.id)