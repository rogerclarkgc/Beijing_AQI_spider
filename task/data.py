# -*- coding: utf-8 -*-
# Author: rogerclark

import pandas
from pandas import DataFrame
import pymongo

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