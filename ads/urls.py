from django.urls import path
from config import settings
from django.conf.urls.static import static

from ads.apps import AdsConfig
from ads.views import ads_filter, ads_lst_with_create, create_ads_confirm, create_proposal_confirm, custom_warning, delete_ads_confirm, delete_prop_confirm, proposals_lst_with_create, update_ads_confirm, update_prop_confirm, warning_ads_not_exits

app_name = AdsConfig.name

urlpatterns = [
    
    path('', ads_lst_with_create, name='ads_lst'),
    path('ads_filter', ads_filter, name='ads_filter'),
    path('create_ads_confirm/<int:pk>', create_ads_confirm, name='create_ads_confirm'),
    path('update_ads_/<int:pk>', update_ads_confirm, name='update_ads_confirm'),
    path('delete_ads/<int:pk>', delete_ads_confirm, name='delete_ads_confirm'),
    path('custom_warning/', custom_warning, name='custom_warning'),
    path('warning_ads_not_exits/', warning_ads_not_exits, name='warning_ads_not_exits'),
    
    path('proposals_lst_with_create', proposals_lst_with_create, name='proposals_lst_with_create'),
    path('create_proposal_confirm/<int:pk>', create_proposal_confirm, name='create_proposal_confirm'),
    path('update_prop_confirm/<int:pk>', update_prop_confirm, name='update_prop_confirm'),
    path('delete_prop_confirm/<int:pk>', delete_prop_confirm, name='delete_prop_confirm'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

