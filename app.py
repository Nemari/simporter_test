import pandas as pd
from datetime import datetime
import numpy as np
import time
import plotly.offline
import plotly.graph_objects as go
import plotly.offline
import json

csv_file='data.csv'
data = pd.read_csv(csv_file)

date = data['timestamp']
event = data['id']

x=list(date)
y=list(event)

def create_plot():
   '''
   This method creates plot using plotly.
   :return: json-plot
   '''
   fig = [go.Bar(
       x=x,
       y=y)]
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return graphJSON


def time_to_utc(s):
    date = time.mktime(datetime.strptime(s, "%m/%d/%Y %H:%M:%S").timetuple())
    return int(date+7200)

def application(startDate, endDate, stars, asin, brand, source, type, grouping):
    '''
    This method does the logic part of the application
    :param startDate: start date
    :param endDate: end date
    :param stars: amount of stars(int)
    :param asin: asin(string)
    :param brand: brand(string)
    :param source: source(string)
    :param type: type of plot(cumulative or usual)
    :param grouping: the way of groupind(weekly, bi-weekly, monthly)
    :return: json-plot
    '''

    csv_file = 'data.csv'
    data = pd.read_csv(csv_file)

    startDate = time_to_utc(startDate)
    endDate = time_to_utc(endDate)

    data = data.query('timestamp >= @startDate & timestamp <= @endDate')  #choosing the timeline
    print(data)
    if stars == None:
        stars = data['stars']
    if asin == None:
        asin = data['asin']
    if brand == None:
        brand = data['brand']
    if source == None:
        source = data['source']

    data = data.query('stars == @stars & asin == @asin & brand == @brand & source == @source') #filtering arguments
    print(data)

    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s') #converting to datetime

    if grouping == 'weekly':
        data['week'] = data['timestamp'].apply(lambda x: "%d" % (x.week))
        data = data.groupby('week').size().reset_index(name='count')
    elif grouping =='bi-weekly':
        data['bi-week'] = data['timestamp'].apply(lambda x: "%d" % ((x.week)*0.5))
        data = data.groupby('bi-week').size().reset_index(name = 'count')
    elif grouping == 'monthly':
        data['month'] = data['timestamp'].apply(lambda x: x.strftime("%m"))
        data = data.groupby('month').size().reset_index(name = 'count')
    print(data.to_json())

    if type == 'cumulative':
        x = list(data[data.columns[0]])
        y =  list(data[data.columns[-1]])
        y = list(np.cumsum(y))
        fig = [go.Bar(
            x=x,
            y=y)]
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    elif type == 'usual':
        x = list(data[data.columns[0]])
        y =  list(data[data.columns[-1]])
        fig = [go.Bar(
            x=x,
            y=y)]
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON


