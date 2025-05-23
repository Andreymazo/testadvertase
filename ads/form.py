
from django import forms

from ads.models import Advertisement, ExchangeProposal

"""Формы для Advertisement"""

class CreateAdsForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'category', 'description', 'image', 'status']

class UpdateAdsForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title',  'category', 'description', 'image', 'status'] 


class DeleteAdsForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['id']  

"""В задании не сказано, что надо фильтровать по айди, но я оставлю,\
    потому-что основная фильтрация по-моему по айди происходит. По -заданию, надо фильтровать по категорнии и по статусу.
    Пагинация всю фильтрацию обнулила. Либо по пагинации скакать, либо фильтрацией выборку делать"""
class FilterAdsForm(forms.Form):
    min_id = forms.IntegerField(label='От', required=False)
    max_id = forms.IntegerField(label='До', required=False)
    category_for_search = forms.CharField(label='Название категории', required=False)
    status_for_search = forms.CharField(label='Статус', required=False)
   
"""Формы для ExchangeProposal"""

class CreateProposalsForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = [ 'ad_receiver', 'comment', 'status', ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     instance = kwargs.get("instance")
    #     if instance:
    #         if instance.ad_receiver:
    #             return instance.id

# class CreateProposalsForm(forms.Form):
    
#     ad_receiver = forms.CharField(label="Your name", max_length=100)

#     class Meta:
#         model = ExchangeProposal
#         fields = [ 'ad_receiver', 'comment', 'status', ]
        

"""По-заданию только статус надо иметь возможность изменить, поэтому остальные поля закомментированы"""
class UpdatePropForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['status',] #'ad_sender', 'ad_receiver', 'comment', 