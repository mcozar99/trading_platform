import sys
sys.path.append('.')
sys.path.append('..')
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from config import INFLUXDB_TOKEN

org = "mcozartramblin@hawk.iit.edu"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

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


'''
def simple_query():
    query_api = client.query_api()

    query = """from(bucket: "currencies")
     |> range(start: -10m)
     |> filter(fn: (r) => r._measurement == "measurement1")"""
    tables = query_api.query(query, org="mcozartramblin@hawk.iit.edu")

    for table in tables:
      for record in table.records:
        print(record)

simple_query()
'''
