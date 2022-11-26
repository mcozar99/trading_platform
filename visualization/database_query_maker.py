import sys
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from config import INFLUXDB_TOKEN
import pandas as pd
from datetime import datetime

sys.path.append('.')
sys.path.append('..')


class QueryMaker:

    def __init__(self):
        """
        The initialization of the class is the creation of an influx client to make the queries
        Parameters are fixed, we are only referring to our specific bucket of currencies
        """
        self.org = "mcozartramblin@hawk.iit.edu"
        self.url = "https://us-east-1-1.aws.cloud2.influxdata.com"
        self.client = influxdb_client.InfluxDBClient(url=self.url, token=INFLUXDB_TOKEN, org=self.org)
        self.bucket = "currencies"


    def currency_simple_query(self, currencies, start, stop):
        """
        Makes a query of several currencies in a certain range of time
        :param currencies: list of the currencies to query
        :param start: time start in format 'yyyy-mm-dd hh:mm'
        :param stop: until format 'yyyy-mm-dd hh:mm'
        :return: pandas dataframe to represent
        """
        start = start.split(' ')[0] + 'T' + start.split(' ')[1] + ':00.597Z'
        stop = stop.split(' ')[0] + 'T' + stop.split(' ')[1] + ':00.597Z'

        # Empty filter
        if len(currencies) == 0:
            return None
        elif len(currencies) == 1:
            filter = 'r["_field"] == "%s"' % currencies[0]
        else:
            filter = 'r["_field"] == "%s"' % currencies[0]
            for item in currencies[1:]:
                filter += ' or r["_field"] == "%s"' % item

        query = """from(bucket: "currencies")
        |> range(start: %s, stop: %s)
        |> filter(fn: (r) => %s) |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")""" % (
            start, stop, filter)
        try:
            return self.client.query_api().query_data_frame(query, org=self.org)
        except Exception as e:
            print(e)
            return None
