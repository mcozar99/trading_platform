import plotly.express as px
import plotly.graph_objects as go
import json
import io
from base64 import b64encode

"""
Falta comparar valores, falta comparar con respecto a otra currency, stream
"""


class Visualizer:

    def __init__(self):
        """
        The initialization has the list of currencies to detect them among the dataframes, and the dictionary
        to print the names of the currencies in the list
        """
        self.currencies = ['ARS', 'AUD', 'BHD', 'BWP', 'BRL', 'BND', 'BGN', 'CAD', 'CLP', 'CNY', 'COP', 'HRK', 'CZK',
                           'DKK', 'EUR', 'HKD', 'HUF', 'ISK', 'INR', 'IDR', 'IRR', 'ILS', 'JPY', 'KZT', 'KRW', 'KWD',
                           'LYD', 'MYR', 'MUR', 'MXN', 'NPR', 'NZD', 'NOK', 'OMR', 'PKR', 'PHP', 'PLN', 'QAR', 'RON',
                           'RUB', 'SAR', 'SGD', 'ZAR', 'LKR', 'SEK', 'CHF', 'TWD', 'THB', 'TTD', 'TRY', 'AED', 'GBP',
                           'VEF', 'USD']
        with open('../data/currency_dictionary.json', 'r') as f:
            self.curr_dict = json.load(f)

    def visualize_several_currencies(self, df):
        """
        Returns visualization of
        :param df:
        :return:
        """
        # Get the currencies that are present on the dataframe
        currencies = []
        for col in df.columns:
            if col in self.currencies:
                currencies.append(col)
        # If there is no currency we return none and if there is we just initialize the figure with first one
        if len(currencies) < 1:
            return None
        else:
            fig = px.line(df, x='_time', y=currencies[0])
            fig['data'][0]['name'] = currencies[0]
            fig['data'][0]['showlegend'] = True
            fig['layout']['xaxis']['title']['text'] = 'Date & Time'
            fig['layout']['yaxis']['title']['text'] = 'Dollars'
        # If it is not 1 we add the rest to the graph
        if len(currencies) != 1:
            for curr in currencies[1:]:
                fig.add_scatter(x=df['_time'], y=df[curr], mode='lines')
                fig['data'][currencies.index(curr)]['name'] = curr
                fig['data'][currencies.index(curr)]['showlegend'] = True
        # We encode the figure to be passed as HTML text
        buffer = io.StringIO()
        fig.write_html(buffer)
        #html_bytes = buffer.getvalue().encode()
        return buffer.getvalue()
