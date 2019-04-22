# -*- coding: utf-8 -*-
# Author: rogerclark

from datetime import date, time, datetime, timedelta

import pandas
from pandas import DataFrame
import pymongo
from ggplot import *

from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

"""
This module will try to store the data in a mongo database,
or just store it in a .csv file
"""

class DataHandler(object):

    def __init__(self):

        self.datalist = None
        self.datatable = None
        self.client = None
        self.db = None
        self.collection = None

    def merge_data(self, datalist):

        self.datatable = DataFrame(datalist)
        return self.datatable

    def connect_database(self, database, collection, host=None, username=None, passwd=None):

        print("Try to connect to {} database".format('remote' if host else 'local'))
        if not host:
            # connect to a local mongoclient
            self.client = pymongo.MongoClient()
        else:
            # connnect to a remote mongoclient
            loginfo = "mongodb://{}:{}@{}".format(username, passwd, host)
            self.client = pymongo.MongoClient(loginfo)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def close_client(self):

        self.client.close()

    def add_in_database(self, datalist):

        if self.check_database_write():
            msg = self.collection.insert_many(datalist)
            print(msg.inserted_ids)
        else:
            raise RuntimeError('The database is not writeable')

    def fetch_from_database(self, query):

        if isinstance(query, dict) is not True:
            raise RuntimeError("query must be a dict object!")


        find_result = self.collection.find(query)
        res_list = list(find_result)
        return [] if len(res_list)==0 else res_list



    def check_database_write(self):

        return self.client._is_writable()

    def add_in_csv(self):
        pass

class DataDrawer(object):

    def __init__(self, database, collection, host=None, username=None, passwd=None):

        print("Try to connect to {} database".format('remote' if host else 'local'))
        if not host:
            # connect to a local mongoclient
            self.client = pymongo.MongoClient()
        else:
            # connnect to a remote mongoclient
            loginfo = "mongodb://{}:{}@{}".format(username, passwd, host)
            self.client = pymongo.MongoClient(loginfo)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def select_data(self, location, pollutant, period=None, acperiod=None):

        if period and not acperiod:
            datasplit = period.split(',')
            if len(datasplit) <= 1:
                t0 = "{}T00:00:00Z".format(datasplit[0])
                t1 = datetime.strptime(datasplit[0], "%Y-%m-%d") + timedelta(days=1)
                t1 ="{}T00:00:00Z".format(t1.strftime("%Y-%m-%d"))
            else:
                t0 = datasplit[0]
                #t1 = datasplit[1]
                t1 = datetime.strptime(datasplit[1], "%Y-%m-%d") + timedelta(days=1)
                t1 = "{}T00:00:00Z".format(t1.strftime("%Y-%m-%d"))
            query = {'location': {'$regex':'{}.*?'.format(location)},
                     'type': pollutant,
                     'data_time': {'$gte': t0,
                                   '$lte': t1}}
        elif acperiod and not period:
            datasplit = period.split(',')
            if len(datasplit) <= 1:
                t0 = "{}T00:00:00Z".format(datasplit[0])
                t1 = datetime.strptime(datasplit[0], "%Y-%m-%d") + timedelta(days=1)
                t1 = "{}T00:00:00Z".format(t1.strftime("%Y-%m-%d"))
            else:
                t0 = datasplit[0]
                #t1 = datasplit[1]
                t1 = datetime.strptime(datasplit[0], "%Y-%m-%d") + timedelta(days=1)
                t1 = "{}T00:00:00Z".format(t1.strftime("%Y-%m-%d"))
            query = {'location': {'$regex': '{}.*?'.format(location)},
                     'type': pollutant,
                     'acquire_time': {'$gte': t0,
                                   '$lte': t1}}
        elif acperiod and period:
            datasplit_p = period.split(',')
            datasplit_ap = acperiod.split(',')
            if len(datasplit_p) <= 1:
                tp0 = "{}T00:00:00Z".format(datasplit_p[0])
                #tp1 = "{}T24:00:00Z".format(datasplit_p[0])
                tp1 = datetime.strptime(datasplit_p[0], "%Y-%m-%d") + timedelta(days=1)
                tp1 = "{}T00:00:00Z".format(tp1.strftime("%Y-%m-%d"))
                tap0 = "{}T00:00:00Z".format(datasplit_ap[0])
                #tap1 = "{}T24:00:00Z".format(datasplit_ap[0])
                tap1 = datetime.strptime(datasplit_ap[0], "%Y-%m-%d") + timedelta(days=1)
                tap1 = "{}T00:00:00Z".format(tap1.strftime("%Y-%m-%d"))

            else:
                tp0 = datasplit_p[0]
                #tp1 = datasplit_p[1]
                tp1 = datetime.strptime(datasplit_p[0], "%Y-%m-%d") + timedelta(days=1)
                tp1 = "{}T00:00:00Z".format(tp1.strftime("%Y-%m-%d"))
                tap0 = datasplit_ap[0]
                #tap1 = datasplit_ap[1]
                tap1 = datetime.strptime(datasplit_ap[0], "%Y-%m-%d") + timedelta(days=1)
                tap1 = "{}T00:00:00Z".format(tap1.strftime("%Y-%m-%d"))
            query = {'location': {'$regex': '{}.*?'.format(location)},
                     'type': pollutant,
                     'data_time': {'$gte': tp0,
                                   '$lte': tp1},
                     'acquire_time': {'$gte': tap0,
                                      '$lte': tap1}}
        elif not period and not acperiod:
            query = {'location': {'$regex': '{}.*?'.format(location)},
                     'type': pollutant}

        find = self.collection.find(query)
        result = list(find)
        return [] if len(result)==0 else result

    def to_dataframe(self, datalist):

        return DataFrame(datalist)


    def remove_duplicate(self, dataframe, subset):

        return dataframe.drop_duplicates(subset=subset)

    def to_numeric(self, dataframe, subset):

        dataframe[subset] = dataframe[subset].apply(pandas.to_numeric, errors='coerce')
        return dataframe

    def to_datatime(self, dataframe, subset):

        dataframe[subset] = dataframe[subset].apply(pandas.to_datetime, errors='coerce')
        return dataframe

    def remove_na(self, dataframe, axis=0):

        dataframe = dataframe.dropna(axis=axis)
        return dataframe

    def wash_data(self, datalist, aqi=False):

        df = self.to_dataframe(datalist)
        df = self.remove_duplicate(df, subset='data_time')
        if aqi:
            df = self.to_numeric(df, subset=['AQI'])
        else:
            df = self.to_numeric(df, subset=['IAQI', 'concentration'])
        df = self.to_datatime(df, subset=['acquire_time', 'data_time'])
        df = self.remove_na(df, axis=0)
        return df

    def draw_line(self, dataframe, aqi=False):

        maintitle = dataframe['location'][0]
        ylb=dataframe['type'][0]
        maintitle = maintitle + '-' + ylb
        unit={'AQI':'',
              'IAQI':'',
              'PM25':'mcg/m^3',
              'PM10':'mcg/m^3',
              'SO2':'mcg/m^3',
              'NO2':'mcg/m^3',
              'O3':'mcg/m^3',
              'CO':'mg/m^3'}
        ylb2 = unit[ylb]
        xlb='date'
        if aqi:
            fig = ggplot(aes(x='data_time',y='AQI'),
                        data=dataframe)
        else:
            fig = ggplot(aes(x='data_time',y='concentration'),
                         data=dataframe)
        fig = fig + geom_line()
        fig = fig + xlab(xlb) + ylab(ylb2) + labs(title=maintitle)
        return fig


    def air_report(self):
        pass


if __name__=='__main__':
    dd = DataDrawer('test', 'air')
    res = dd.select_data('永定门','SO2','2019-04-21')
    df = dd.wash_data(res,aqi=False)
    fig = dd.draw_line(df,aqi=False)
    print(fig)