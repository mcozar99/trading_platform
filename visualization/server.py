import sys
from flask import Flask, request, stream_with_context
from database_query_maker import QueryMaker
from visualization import Visualizer
import time
import pandas as pd

sys.path.append('.')
sys.path.append('..')

app = Flask(__name__)
query_maker = QueryMaker()
visualizer = Visualizer()


"""
$ export FLASK_APP=hello.py
$ python -m flask run
flask run --host=0.0.0.0
"""


@app.route('/', methods=['GET'])
def initial():
    output = """
    <h1>Final Project,</h1>
    <h2>Miguel Cozar Tramblin \t A20522001</h2>
    <h3>Big Data Technologies: Currency Trading Platform </h3
    List of currencies supported:
    <ul>
    """
    for item in visualizer.curr_dict:
        output += "<li>%s: %s</li>"%(item, visualizer.curr_dict[item])
    output += "</ul>"
    return output


@app.route('/currency', methods=['GET'])
def visualize_currency():
    """Returns a visualization plot of requested currencies"""
    args = request.args
    df = query_maker.currency_simple_query(args.get('currencies').split(', '), args.get('start'), args.get('stop'))
    figure = visualizer.visualize_several_currencies(df)
    if figure is not None:
        out = """
        <h1>Visualization of %s from %s to %s</h1>
        %s
        """%(args.get('currencies'), args.get('start'), args.get('stop'), figure)
        return out
    return 'No data available or bad requested'


@app.route('/latest', methods=['GET'])
def latest_values():
    """Returns a chart of the requested values"""
    args = request.args
    df = query_maker.get_latest_values(args.get('currencies').split(', '))
    if df is not None:
        time = df.sample().time.item().strftime('%Y-%m-%d %H:%M')
        df.drop('time', axis=1, inplace=True)
        out = """
        <h1>Latest Values of requested currencies at %s</h1>
        %s
        """%(time, df.to_html(classes='table table-stripped'))
        return out
    return 'No data available or bad requested'


@app.route('/stream', methods=['GET'])
def stream():
    def generate():
        for i in range(10):
            yield str(i)
            yield '!'
            time.sleep(1)
    return app.response_class(stream_with_context(generate()))


