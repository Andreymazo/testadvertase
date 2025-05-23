from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from ads.form import CreateAdsForm, CreateProposalsForm, DeleteAdsForm, FilterAdsForm, UpdateAdsForm, UpdatePropForm
from ads.models import Advertisement, ExchangeProposal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from users.models import CustomUser


"""Список объявлений. Форма создания сверху"""
def ads_lst_with_create(request):
    if request.user.is_anonymous:
        return redirect('users:log_in')
        
    ads_queryset = Advertisement.objects.all()
    form = CreateAdsForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            ads_instance = Advertisement(user=CustomUser.objects.get(id=request.user.id), **form.cleaned_data)
            ads_instance.save()
            return redirect(reverse('ads:create_ads_confirm', kwargs={'pk':ads_instance.id}))
    else:
        form = CreateAdsForm()

    context = {'form': form,
               'ads_queryset':ads_queryset}
    return render(request, 'ads/templates/ads_lst.html', context)


"""Подтверждение создания объявления"""
def create_ads_confirm(request, **kwargs):
    pk=kwargs['pk']
    context ={}
    try:
        new_ads_obj = Advertisement.objects.get(id=pk)
        context = {'new_ads_obj':new_ads_obj,
                   "user":request.user}
    except:
        Advertisement.DoesNotExist
        return redirect('ads:ads_lst')
        
    return render(request, 'ads/templates/create_ads_confirm.html', context)


"""Редактирование объявления"""
def update_ads_confirm(request, pk):
    instance = Advertisement.objects.get(id=pk)
    context = {"form": UpdateAdsForm(initial={"id":instance.id, "title": instance.title, "image": instance.image,\
                    "category":instance.category, "description": instance.description}),"ads": instance, }
    
    if request.method == "GET":
        return render(request,"ads/templates/update_ads.html",context)
    
    elif request.method == "POST":
        if not instance.user==request.user:
            return HttpResponseRedirect(reverse('ads:custom_warning'))
        form = UpdateAdsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse('ads:create_ads_confirm', kwargs={'pk':form.instance.id}))
    return render(request, 'ads/templates/update_ads.html', context)


"""Ендпоинт - Предупреждение, если нет права."""
def custom_warning(request, **kwargs):
    context = {}
    return render(request, 'ads/templates/custom_warning.html', context)


"""Ендпоинт - Предупреждение, если нет объекта."""   
def warning_ads_not_exits(request, **kwargs):
    context = {}
    return render(request, 'ads/templates/warning_ads_not_exits.html', context)


"""Удаление объявления"""
def delete_ads_confirm(request, pk):
    try:
        instance = Advertisement.objects.get(id=pk)
    except Advertisement.DoesNotExist:
        return redirect('ads:warning_ads_not_exits')
    if request.method == 'POST':
        if not instance.user==request.user:
            return HttpResponseRedirect(reverse('ads:custom_warning'))
        form = DeleteAdsForm(request.POST, instance=instance)
        if form.is_valid():
            instance.delete()
            return HttpResponseRedirect(reverse("ads:ads_lst"))
    else:
        form = DeleteAdsForm(instance=instance)
    context ={"form":form}
    return render(request, 'ads/templates/delete_ads.html', context)


"""Фильтрация по категории и состоянию товара. Фильтруем и по айди. Пагинация, \
    без которой все фильтрация работает и с которой наоборот, не работатет."""
def ads_filter(request):
    
    if request.user.is_anonymous:
        return redirect('users:log_in')
    form = FilterAdsForm(request.POST, request.FILES)
    ads_queryset = Advertisement.objects.all()
    p = Paginator(ads_queryset, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number) 
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
   

    if form.is_valid():
        min_id_value = form.cleaned_data['min_id']
        max_id_value = form.cleaned_data['max_id']
        category_for_search_value = form.cleaned_data['category_for_search']
        status_for_search_value = form.cleaned_data['status_for_search']
        if form.cleaned_data['min_id']:
                    ads_queryset=ads_queryset.filter(id__gte=min_id_value)
        if form.cleaned_data['max_id']:
            ads_queryset=ads_queryset.filter(id__lte=max_id_value)
            
        if form.cleaned_data['category_for_search']:
            ads_queryset=ads_queryset.filter(category=category_for_search_value)
        if form.cleaned_data['status_for_search']:
            ads_queryset=ads_queryset.filter(status=status_for_search_value)
        if form.cleaned_data['category_for_search'] and form.cleaned_data['status_for_search'] and form.cleaned_data['max_id']\
              and form.cleaned_data['min_id']:
            ads_queryset=ads_queryset.filter(id__gte=min_id_value).filter(id__lte=max_id_value).\
                filter(category=category_for_search_value).filter(status=status_for_search_value)
        if form.cleaned_data['category_for_search'] and form.cleaned_data['max_id'] :
            ads_queryset=ads_queryset.filter(id__lte=max_id_value).filter(category=category_for_search_value)
        if form.cleaned_data['category_for_search'] and form.cleaned_data['min_id']:
            ads_queryset=ads_queryset.filter(id__gte=min_id_value).filter(category=category_for_search_value)
        if form.cleaned_data['status_for_search'] and form.cleaned_data['max_id'] :
            ads_queryset=ads_queryset.filter(id__lte=max_id_value).filter(status=status_for_search_value)
        if form.cleaned_data['status_for_search'] and form.cleaned_data['min_id']:
            ads_queryset=ads_queryset.filter(id__gte=min_id_value).filter(status=status_for_search_value)
        context = {'form': form,
               'ads_queryset':ads_queryset,
               'page_obj': page_obj}
        
    return render(request, 'ads/templates/ads_filtere_lst.html', context)


"""Список Предложений. Форма создания сверху"""
def proposals_lst_with_create(request):
    if request.user.is_anonymous:
        return redirect('users:log_in')
        
    prop_queryset = ExchangeProposal.objects.all()
    form = CreateProposalsForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            prop_instance = ExchangeProposal(ad_sender=CustomUser.objects.get(id=request.user.id), **form.cleaned_data)
            prop_instance.save()
            return redirect(reverse('ads:create_proposal_confirm', kwargs={'pk':prop_instance.id}))
    else:
        form = CreateProposalsForm()

    context = {'form': form,
               'prop_queryset':prop_queryset,
               'user':request.user}
    return render(request, 'ads/templates/proposals_lst_with_create.html', context)


"""Подтверждение создания предложения"""
def create_proposal_confirm(request, **kwargs):
    pk=kwargs['pk']
    context ={}
    try:
        new_prop_obj = ExchangeProposal.objects.get(id=pk)
        context = {'new_prop_obj':new_prop_obj,
                   "user":request.user}
    except:
        ExchangeProposal.DoesNotExist
        return redirect('ads:proposals_lst_with_create')
        
    return render(request, 'ads/templates/create_prop_confirm.html', context)


"""Редактирование предложения"""
def update_prop_confirm(request, pk):
    instance = ExchangeProposal.objects.get(id=pk)
    context = {"form": UpdatePropForm(initial={"id":instance.id, "ad_sender": instance.ad_sender, "ad_receiver": instance.ad_receiver,\
                    "comment":instance.comment, "status": instance.status}),"prop": instance, }
    
    if request.method == "GET":
        return render(request,"ads/templates/update_ads.html",context)
    
    elif request.method == "POST":
        if not instance.ad_sender==request.user:
            return HttpResponseRedirect(reverse('ads:custom_warning'))
        form = UpdatePropForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            prop_instance = form.save(commit=False)
            prop_instance.status = form.cleaned_data['status']
            prop_instance.save()
            # form.save()
            return redirect(reverse('ads:create_proposal_confirm', kwargs={'pk':form.instance.id}))
    return render(request, 'ads/templates/update_prop.html', context)


"""Удаление объявления"""
def delete_prop_confirm(request, pk):
    try:
        instance = ExchangeProposal.objects.get(id=pk)
    except ExchangeProposal.DoesNotExist:
        return redirect('ads:warning_ads_not_exits')
    if request.method == 'POST':
        if not instance.ad_sender==request.user:
            return HttpResponseRedirect(reverse('ads:custom_warning'))
        form = DeleteAdsForm(request.POST, instance=instance)
        if form.is_valid():
            instance.delete()
            return HttpResponseRedirect(reverse("ads:proposals_lst_with_create"))
    else:
        form = DeleteAdsForm(instance=instance)
    context ={"form":form}
    return render(request, 'ads/templates/delete_prop.html', context)