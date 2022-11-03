import sys

sys.path.append('.')
sys.path.append('..')
import pandas as pd
import json
from utils import get_current_datetime, datetime_to_timestamp, add_minutes_to_date
from database.influx import write_stream_data
from datetime import datetime
import pause


class StreamCollector:

    def __init__(self):
        """
        Parameters fixed are a dictionary with the currency keys, the url of the site to scrap and the currency values
        """
        self.url = 'https://www.x-rates.com/table/'
        self.currencies = ['ARS', 'AUD', 'BHD', 'BWP', 'BRL', 'BND', 'BGN', 'CAD', 'CLP', 'CNY', 'COP', 'HRK', 'CZK',
                           'DKK', 'EUR', 'HKD', 'HUF', 'ISK', 'INR', 'IDR', 'IRR', 'ILS', 'JPY', 'KZT', 'KRW', 'KWD',
                           'LYD', 'MYR', 'MUR', 'MXN', 'NPR', 'NZD', 'NOK', 'OMR', 'PKR', 'PHP', 'PLN', 'QAR', 'RON',
                           'RUB', 'SAR', 'SGD', 'ZAR', 'LKR', 'SEK', 'CHF', 'TWD', 'THB', 'TTD', 'TRY', 'AED', 'GBP',
                           'VEF', 'USD']
        with open('data/currency_dictionary.json', 'r') as f:
            self.curr_dict = json.load(f)

    def scrap(self):
        """
        Scraps the url for getting the data
        :return: a raw response
        """
        try:
            return pd.read_html(self.url)
        except Exception as e:
            print(e)
            return None

    def format_data(self, df):
        """
        Parses the response to get the dataframe expected
        :return: a series with the formatted data
        """
        try:
            df = df[1]
            df.loc[len(df), :] = ['US Dollar', 1, 1]
            df.rename(columns={'US Dollar': 'currency', '1.00 USD': 'value', 'inv. 1.00 USD': 'a'}, inplace=True)
            df.drop('a', axis=1, inplace=True)
            df.currency = df.currency.apply(lambda x: self.curr_dict[x])
            return dict(zip(df.currency, df.value))
        except Exception as e:
            print(e)
            return None

    def get_currency_values(self):
        """
        Combines previous functions to get a row of currency data
        :return:
        """
        return self.format_data(self.scrap())

    def streaming(self, sweep_period=5, stop_time='2100-12-31 12:00'):
        """
        Gathers streaming data from the url provided
        :param sweep_period: time in minutes for scrapping from 1 minute to x
        :param stop_time: date to stop in format 'yyyy-mm-dd hh:mm'
        """

        while True:
            # Add current forex values to InfluxDB
            row = self.get_currency_values()
            current_time = get_current_datetime()
            write_stream_data(row)

            # If we reached stop time then we save & stop the streaming
            if datetime_to_timestamp(stop_time) < datetime_to_timestamp(current_time):
                # Not needed anymore
                # df.to_csv('data/%s' % data_name, index=True)
                break

            # Sleep until a new update comes (we operate at half of each minute to let the page refresh)
            pause.until(
                datetime.strptime(add_minutes_to_date(current_time, sweep_period), '%Y-%m-%d %H:%M').replace(second=30))
