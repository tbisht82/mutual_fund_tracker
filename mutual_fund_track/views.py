from django.shortcuts import render, redirect, get_object_or_404
from .models import MutualFund, MutualFundValue
from .forms import MutualFundForm
from django.contrib import messages
from django.http import JsonResponse
import datetime


def add_new_isin(request):
    '''
        Adding new ISIN from filled form
    '''
    if request.method == 'POST':
        form = MutualFundForm(request.POST)
        if form.is_valid():
            isin = form.cleaned_data['ISIN']
            mf = MutualFund(ISIN=isin)
            mf.save()
            messages.success(request, 'Mutual fund ISIN added successfully')
        else:
            messages.error(request, form.errors.get('ISIN')[0])
    
    mf = MutualFund.objects.filter(ISIN='INF204K01HY3')
    mfvc = MutualFundValue.objects.filter(mutual_fund=mf).count()

    context = {'form': MutualFundForm,
            'mf': mf,
            'mfvc': mfvc
        }
    return render(request, 'add_mutual_fund.html', context)


def detail_isin(request, isin):
    '''
        Getting details of a mutual fund using ISIN
    '''
    mutual_fund = get_object_or_404(MutualFund, pk=isin)
    first = MutualFundValue.objects.filter(
        mutual_fund=mutual_fund).values_list('date', 'value').first()
    last = MutualFundValue.objects.filter(
        mutual_fund=mutual_fund).values_list('date', 'value').last()

    if first is None:
        context = {
            'mutual_fund': mutual_fund,
            'all_years': False,
        }
        return render(request, 'mutual_fund_details.html', context)

    timestamp = timestamp = datetime.date.fromtimestamp(first[0]/1000)
    date = timestamp.strftime('%d-%m-%Y')
    
    start = int(date.split('-')[2])

    timestamp = timestamp = datetime.date.fromtimestamp(last[0]/1000)
    date = timestamp.strftime('%d-%m-%Y')
    
    end = int(date.split('-')[2])

    all_years = [i for i in range(start, end+1)]

    context = {
        'mutual_fund': mutual_fund,
        'all_years': all_years,
    }
    return render(request, 'mutual_fund_details.html', context)


def chart_data(request, isin):
    '''
        Getting mutual fund data for chart generation
    '''
    print(isin)
    isin_year = isin.split('-')
    years = []
    if len(isin_year)==3:
        years = [str(i) for i in range(int(isin_year[1]),int(isin_year[2])+1)]
    
    mutual_fund = get_object_or_404(MutualFund, pk=isin_year[0])
    data = MutualFundValue.objects.filter(
        mutual_fund=mutual_fund).values_list('date', 'value')
    complete_data = []
    for item in data:
        timestamp = timestamp = datetime.date.fromtimestamp(item[0]/1000)
        date = timestamp.strftime('%d-%m-%Y')
        complete_data.append((date, item[1]))

    labels = []
    values = []
    print(years)

    for year in years:
        for item in complete_data:
            if year in item[0].split('-'):
                labels.append(item[0])
                values.append(item[1]) 

    return JsonResponse(data={
        'labels': labels,
        'data': values,
    })


def search(request):
    '''
        Search mutual fund on the basis of provided ISIN in search bar
    '''
    isin = request.GET['isin']
    print(isin)
    return redirect('details_isin', isin=isin)


def delete(request):
    mf = MutualFund.objects.filter(ISIN='INF204K01HY3')
    mfvc = MutualFundValue.objects.filter(mutual_fund=mf).last()

    mfvc.delete()
    return render(request, 'new_isin')
