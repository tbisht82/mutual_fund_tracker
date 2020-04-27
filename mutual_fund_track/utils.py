import requests
import csv
import os
from .models import MutualFund, MutualFundValue

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def download_mutual_fund_file():
    '''
        Method to download csv file from the below URL
    '''
    data = requests.get("https://amberja.in/wp-content/uploads/2020/01/isin_list.csv")
    filename = BASE_DIR + "/downloads/mutual.csv"
    with open(filename,'wb+') as f:
        f.write(data.content)

    mutual_funds = set()

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader: 
            mutual_funds.add(row[0])
        
    return mutual_funds


def get_mutual_funds_from_db():
    '''
        Reading all the mutual funds from DB
    '''
    data = MutualFund.objects.all().values_list()
    mutual_funds_in_db = set()

    for item in data:
        mutual_funds_in_db.add(item[0])

    return mutual_funds_in_db


def save_new_mutual_funds_db(mutual_funds_db, mutual_funds_csv):
    '''
        Saving New mutual funds given in csv file to db
    '''
    mutual_funds_to_be_saved = mutual_funds_csv - mutual_funds_db
    insert_data = []
    for item in mutual_funds_to_be_saved:
        isin = str(item)
        insert_data.append(MutualFund(ISIN=isin))
    MutualFund.objects.bulk_create(insert_data)
    save_new_mutual_fund_values(mutual_funds_to_be_saved)


def save_new_mutual_fund_values(mutual_funds=None):
    '''
        Saving and updating new mutual fund NAV
    '''
    if mutual_funds is None:
        mutual_funds = get_mutual_funds_from_db()
    for mutual_fund in mutual_funds:
        status_code, legal_name, graph_data = get_mutual_fund_latest_values(mutual_fund)
        if status_code == 200:
            graph_data.sort(key = lambda x: x[0])
            last_stored_values_for_mutual_fund = MutualFundValue.objects.filter(mutual_fund=mutual_fund).values_list('date', 'value').order_by('date').last()
            if last_stored_values_for_mutual_fund is not None:
                try:
                    index = graph_data.index(list(last_stored_values_for_mutual_fund)) + 1
                except ValueError:
                    index = 0
            else:
                index = 0
            insert_data = []
            current_fund = MutualFund.objects.get(ISIN=str(mutual_fund))
            if current_fund.name is None:
                current_fund.name = legal_name
                current_fund.save()
            for item in graph_data[index:]:
                date = int(item[0])
                value = float(item[1])
                insert_data.append(MutualFundValue(mutual_fund=current_fund, date=date, value=value))
            MutualFundValue.objects.bulk_create(insert_data)
        continue


def get_mutual_fund_latest_values(isin):
    '''
        Getting NAV for mutual fund using the below api
    '''
    url = "https://my.fisdom.com/api/funds/moreinfoonfund/" + isin
    data = requests.get(url)
    content = data.json()
    status_code = content['pfwresponse']['status_code']
    if status_code == 200:
        legal_name = content['pfwresponse']['result']['fundinfo']['legal_name']
        graph_data_for_amfi = content['pfwresponse']['result']['fundinfo']['graph_data_for_amfi']
    else:
        legal_name = None
        graph_data_for_amfi = None
    return (status_code, legal_name, graph_data_for_amfi)
