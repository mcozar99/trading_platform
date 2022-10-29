import argparse
import sys


if __name__ == '__main__':
    # For stream collector actions
    p = argparse.ArgumentParser(description='System Orders')
    p.add_argument('--action', required=True, help='Select action among possibilities: [StreamCollector]')

    # Arguments for stream collector
    p.add_argument('--frequency', required=False, default=1, type=int, help='Set the frequency of the data collected '
                                                                            'in minutes')
    p.add_argument('--stoptime', required=False, default='2100-12-31 12:00', nargs=2, type=str, help="date to stop in format "
                                                                                            "'yyyy-mm-dd hh:mm'")
    p.add_argument('--filename', required=False, default='currency_values.csv', type=str, help="Name of the file "
                                                                                               "where we save the "
                                                                                               "data with .csv "
                                                                                               "extension")

    # We parse the argument
    args = vars(p.parse_args())
    # We join stoptime arg if exists
    if type(args['stoptime']) == list:
        args['stoptime'] = ' '.join(args['stoptime'])


    # Select action
    if args['action'] == 'stream':
        from data_collector.data_collector import StreamCollector
        StreamCollector().streaming(sweep_period=args['frequency'], stop_time=args['stoptime'], data_name=args['filename'])

