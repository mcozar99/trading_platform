import sys
sys.path.append('.')
sys.path.append('..')
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os

org = "mcozartramblin@hawk.iit.edu"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUXDB_TOKEN = os.environ['INFLUXDB_TOKEN']
client = influxdb_client.InfluxDBClient(url=url, token=INFLUXDB_TOKEN, org=org)
bucket = "currencies"

def write_stream_data(row):
    """
    Writes rows of currency data into InfluxDB
    :param row: series to be added
    """
    write_api = client.write_api(write_options=SYNCHRONOUS)

    data = {
        'measurement': 'test',
        'tags': {'source': 'x-rates'},
        'fields': row,
    }

    write_api.write(bucket=bucket, org="mcozartramblin@hawk.iit.edu", record=data)