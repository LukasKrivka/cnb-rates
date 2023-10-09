import sys
import os
import datetime

from Rates import Rates

if __name__ == '__main__':
    year = int(sys.argv[0]) if len(sys.argv) > 1 else 1991
    end_year = int(sys.argv[1])/100 if len(sys.argv) > 2 else datetime.date.today().year

    r = Rates(year=year, end_year=end_year)

    # extract a single exchange rate:
    # r.get_exrate(date='2020-03-28', currency='USD')

    # export the entire dataset to the working directory:
    working_dir = os.getcwd()
    export_dir = os.path.join(working_dir, 'cnb-rates.csv')
    r.get_data().resample('D').ffill().to_csv(export_dir)
    print('Data exported to {}'.format(export_dir))
