import sys
sys.path.append('.')
sys.path.append('..')
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.warnings import MissingPivotFunction
import pandas as pd
import json
import warnings

# Warning clean
warnings.simplefilter("ignore", MissingPivotFunction)

INFLUXDB_TOKEN = os.environ['INFLUXDB_TOKEN']

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
        self.currency_symbols = ['ARS', 'AUD', 'BHD', 'BWP', 'BRL', 'BND', 'BGN', 'CAD', 'CLP', 'CNY', 'COP', 'HRK', 'CZK',
                           'DKK', 'EUR', 'HKD', 'HUF', 'ISK', 'INR', 'IDR', 'IRR', 'ILS', 'JPY', 'KZT', 'KRW', 'KWD',
                           'LYD', 'MYR', 'MUR', 'MXN', 'NPR', 'NZD', 'NOK', 'OMR', 'PKR', 'PHP', 'PLN', 'QAR', 'RON',
                           'RUB', 'SAR', 'SGD', 'ZAR', 'LKR', 'SEK', 'CHF', 'TWD', 'THB', 'TTD', 'TRY', 'AED', 'GBP',
                           'VEF', 'USD']
        with open('../data/currency_dictionary.json', 'r') as f:
            self.currency_names = json.load(f)

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
            fields = 'r["_field"] == "%s"' % currencies[0]
        else:
            fields = 'r["_field"] == "%s"' % currencies[0]
            for item in currencies[1:]:
                fields += ' or r["_field"] == "%s"' % item

        query = """from(bucket: "currencies")
        |> range(start: %s, stop: %s)
        |> filter(fn: (r) => %s) |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")""" % (
            start, stop, fields)
        try:
            return self.client.query_api().query_data_frame(query, org=self.org)
        except Exception as e:
            print(e)
            return None

    def get_latest_values(self, currencies):
        """Gets a table with the latest values of a given list if currencies"""
        # Parse Currency List
        if len(currencies) == 0:
            return None
        elif len(currencies) == 1:
            fields = 'r["_field"] == "%s"' % currencies[0]
        else:
            fields = 'r["_field"] == "%s"' % currencies[0]
            for item in currencies[1:]:
                fields += ' or r["_field"] == "%s"' % item

        query = """from(bucket: "currencies")
          |> range(start: -2m)
          |> filter(fn: (r) => %s)
          |> last()
          |> yield(name: "last")
        """ % fields

        try:
            df = self.client.query_api().query_data_frame(query, org=self.org)
        except Exception as e:
            print(e)
            return None
        out = pd.DataFrame({'time': df._time, 'Currency Symbol': df._field})
        out['Currency Name'] = df._field.apply(lambda x: list(self.currency_names.keys()) [list(self.currency_names.values()).index(x)])
        out['value'] = df._value
        return out
