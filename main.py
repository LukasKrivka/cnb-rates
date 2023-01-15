import sys
import datetime

from Rates import Rates

if __name__ == '__main__':
    year = int(sys.argv[0]) if len(sys.argv) > 1 else 1991
    end_year = int(sys.argv[1])/100 if len(sys.argv) > 2 else datetime.date.today().year

    r = Rates(year=year, end_year=end_year)

    # extract a single exchange rate:
    # r.get_exrate(date='2020-03-28', currency='USD')

    # get the exchange rate fraction for Russian Rubl:
    # r.get_exrate_info(currency='RUB')

    # export the entire dataset to current directory:
    r.to_csv(filled=True)
