from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
import pandas as pd 
import plotly.graph_objects as go 
import base64
import matplotlib.pyplot as plt
from plotly.io import to_image

open = []
close = []
high = []
low = []
volume = []


def index(request):
    stock_name = 'IBM'
    time_frame = '1D'
    if 'stockname' in request.POST:
        stock_name = request.POST['stockname']
        print(stock_name)
    if '1min' in request.POST:
        time_frame = '1min'
    elif '5min' in request.POST:
        time_frame = '5min'
    elif '15min' in request.POST:
        time_frame = '15min'
    elif '60min' in request.POST:
        time_frame = '60min'
    elif '30min' in request.POST:
        time_frame = '30min'
    elif '1D' in request.POST:
        time_frame = '1D'
    elif '1W' in request.POST:
        time_frame = '1W'
    elif '1M' in request.POST:
        time_frame = '1M'
    def get_stock_data(stock_name, time_frame):
        if time_frame in ('1min','5min','15min','30min','60min'):
            URL = 'https://www.alphavantage.co/query'
            PARAMS = {'function':'TIME_SERIES_INTRADAY',
                'symbol':stock_name,
                'interval':time_frame,
                'apikey':'demo'
                }
            time_frame_string = 'Time Series ('+ time_frame +')'
        elif time_frame in ('1D'):
            URL = 'https://www.alphavantage.co/query'
            PARAMS = {'function':'TIME_SERIES_DAILY',
                'symbol':stock_name,
                'apikey':'demo'
                }
            time_frame_string = 'Time Series (Daily)'
        elif time_frame in ('1W'):
            URL = 'https://www.alphavantage.co/query'
            PARAMS = {'function':'TIME_SERIES_WEEKLY',
                'symbol':stock_name,
                'apikey':'demo'
                }
            time_frame_string = 'Weekly Time Series'
        elif time_frame in ('1M'):
            URL = 'https://www.alphavantage.co/query'
            PARAMS = {'function':'TIME_SERIES_MONTHLY',
                'symbol':stock_name,
                'apikey':'demo'
                }
            time_frame_string = 'Monthly Time Series'
        req = requests.get(url=URL, params = PARAMS)
        data  = req.json()
        time = [j for j in data[time_frame_string]]
        stock = data[time_frame_string].values()
        valued = [i for i in stock]
        for i in valued:
            a = i["1. open"]
            open.append((float(a)))
            b = i["2. high"]
            high.append((float(b)))
            c = i["3. low"]
            low.append((float(c)))
            d = i["4. close"]
            close.append((float(d)))
            e = i["5. volume"]
            volume.append((float(e))) 
        datasets = []
        for h in range(len(time)):
            sets = {'label' : time[h],
                'y' :[round(open[h],2),round(high[h],2),round(low[h],2),round(close[h],2)]
                   }   
            datasets.append(sets)
        return datasets[::-1]
    datasets = get_stock_data(stock_name,time_frame)        
    return render(request,"index.html",{'time_frame':time_frame,"sets":datasets})


