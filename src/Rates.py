import pandas as pd
import requests
import os
import warnings
import datetime

from typing import Union, List


def _check_date_type(date, date_format: str = None) -> pd.Timestamp:
    """Check if the date datatype or string format and return correct object to search for the data

    :param: date: date passed from user to be checked.
    :param: format: a custom format if the date string is not automatically recognized by parser.
    """

    if isinstance(date, pd.Timestamp) or isinstance(date, pd._libs.tslibs.timestamps.Timestamp):
        return date

    elif isinstance(date, str):
        return pd.to_datetime(date, format=date_format)

    else:
        try:
            return pd.to_datetime(date)
        except Exception as e:
            raise TypeError(
                f"date or end_date parameter must be pandas Timestamp object or str, "
                f"but got {type(date)} instead, which could not be parsed")


class Rates:
    """Rates class contains data for specified time range about Exchange rates published by
    Central Bank of Czech republic."""

    def __init__(self, year: int = None, end_year: int = None):
        """Initiate the class by retrieving requested years from CNB website and save the data in pandas DataFrame
         for later retrieval."""

        self.exrates: dict = {}
        self.data = pd.DataFrame()
        self.ascend = True

        # if year is not provided, fetch data only for the current year
        if year is None:
            year = datetime.date.today().year
        # if end_year is not provided, fetch data only for the specified 'year'
        if end_year is None:
            end_year = year

        # handle requested years outside of range (if possible range is narrowed down)
        if year > datetime.date.today().year:
            raise ValueError(f'year {year} is outside of possible range, higher then current year'
                             f' - no later data to extract')
        if end_year > datetime.date.today().year:
            raise ValueError(f'end year {end_year} is outside of possible range, lower than the starting value 1991'
                             f' - no previous data to extract')
        if year < 1991:
            warnings.warn(f'year {year} is outside of possible range. Lowest possible value (1991) is selected')
            year = 1991
        if end_year > datetime.date.today().year:
            warnings.warn(f'end year {end_year} is outside of possible range. '
                          f'Highest possible value {datetime.date.today().year} is selected')
            end_year = datetime.date.today().year

        # fetch data from cnb website for each year requested
        for i, y in enumerate(range(year, end_year + 1)):
            if i == 0:
                response_list = requests.get('https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu'
                                             '/kurzy-devizoveho-trhu/rok.txt?rok=' + str(y)).text.split("\n")[:-1]
                self.data = self._create_df(response_list)
                continue

            self.add_data(y)

    def _create_df(self, response_list) -> pd.DataFrame:
        """Create dataframe containing exchange rates for a single year response.

        :param response_list: list of rows from requested url retrieved from CNB (rows=dates, columns=currencies).
        """

        df = pd.DataFrame(columns=[])
        for i, row in enumerate(response_list):
            # for the first iteration (first row) handle only currency columns for df creation
            if i == 0:
                curr = []
                for j in row.split("|")[1:]:
                    rate = j.split(" ")
                    curr.append(rate[1])
                    if rate[1] not in self.exrates.keys():
                        # save the exchange rates nominals into private field, only as supplement information
                        self.exrates[rate[1]] = int(rate[0])
                for c in curr:
                    df[c] = None
                continue

            # any other than the first iteration, load the exrates into the DataFrame
            date_info = row.replace(',', '.').split("|")
            # cal_date = date_info[0].split(".")  # Deprecated, not needed anymore, will be removed in future
            # if start of the line is less than 6 characters, it is not a date but a separate frame format (new curr)
            if len(date_info[0]) < 6:
                df = pd.concat([df, self._create_df(response_list[i:])])
                break
            df.loc[pd.to_datetime(date_info[0], format='%d.%m.%Y')] = pd.to_numeric(date_info[1:])

        return df

    def add_data(self, year: int) -> None:
        """Add data for another year of data to the dataset.

        :param year: int specifying what year should be added from CNB data.
        """

        # check if requested year is already included or outside possible range
        if year in self.data.index.year:
            print(f"year {year} is already included in the dataset")
            return
        if year < 1991 or year > datetime.date.today().year:
            print(f"year {year} is outside of possible range (1991 - {datetime.date.today().year})")
            return

        response_list = requests.get('https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu'
                                     '/kurzy-devizoveho-trhu/rok.txt?rok=' + str(year)).text.split("\n")[:-1]
        self.data = pd.concat([self.data, self._create_df(response_list)], axis=0)
        self.data.sort_index(inplace=True, kind='mergesort', ascending=self.ascend)
        del response_list

    def sort(self, ascend: bool = True) -> None:
        """Sort data in dataframe, mainly for exporting purposes.

        The required sort will be saved for newly added years.

        :param ascend: bool, default=True, indicating how dataframe should be sorted.
        """

        self.data.sort_index(inplace=True, kind='mergesort', ascending=ascend)
        self.ascend = ascend

    def get_data(self) -> pd.DataFrame():
        """Get entire data set as pandas DataFrame."""
        return self.data

    def get_exrate_info(self, currency: str) -> int:
        """Return the nominal exchange rate for specified currency.

        :param currency: string, capital three letter abbreviation for currency used by CNB
        (same as columns in DataFrame)
        """
        print(f"Exchange rate is amount of CZK obtained for {self.exrates[currency]} {currency}")
        return self.exrates[currency]

    def get_all_exrate_info(self) -> dict:
        """Return the nominal exchange rates information for all the currencies stored in private field."""
        return self.exrates

    def _get_valid_date(self, date, date_format: str = None) -> pd.Timestamp:
        """Check if requested date is within dataset index range and return valid date
        or raise error if date is outside the range.

        If the date is not in the range of years fetched from CNB website, raise ValueError.
        If the date is in the range, but the datapoint is missing,
        return closest previous date (closest next date in case there is no previous date in the dataset).
        Should be used, after _check_date_type for correct type passing.

        :param date: pandas Timestamp object or String that was requested.
        :param: date_format: a custom format if the date string is not automatically recognized by parser.
        """

        date = _check_date_type(date=date, date_format=date_format)

        # Case: requested date is outside the range fetched from CNB website
        if date.year < self.data.index.min().year or date.year > self.data.index.max().year:
            raise ValueError(f'requested date {date} is not in the retrieved year range. '
                             f'Make sure the year {date.year} in in the specified range, when creating Rates object '
                             f'or add the year using Rates.add_data(year)')

        # Case: requested date is within the range, but is smaller than all the entries,
        # so no previous valid value exists (returns the next value instead)
        if date < self.data.index.min():
            warnings.warn(f"Date {date} is smaller than the smallest value in the central bank dataset.{os.linesep}"
                          f"Closest next date is selected for valid ex. rate. {os.linesep}"
                          f"to get the closest previous value as a valid ex. rate, include data for previous year")
            return self.data.index[self.data.index.get_indexer([date], method='bfill')[0]]

        # Case: requested date is within the range but the value might be missing because of weekends or holidays.
        # Closest previous value is selected as valid exchange rate
        if date not in self.data.index:
            warnings.warn(f"Date {date} is not included in the central bank dataset.{os.linesep}"
                          f"Closest previous date is selected for valid ex. rate")
        return self.data.index[self.data.index.get_indexer([date], method='ffill')[0]]

    def get_exrate(self, date, end_date=None, date_format: str = None, currency: Union[str, List[str]] = None,
                   filled: bool = False) -> Union[int, pd.Series, pd.DataFrame]:
        """Returns exchange rate for specified currency/currencies at specific date or time range.

        If the data are sorted in descending order and a range of dates is requested,
        the date and end_date should still be provided in chronological order,
        but returned slice will be in descending order.

        :param date: pandas Datetime object or a str for which is should return exchange rate. Assumed string format
        is strftime. Other formats may also be accepted by the parser, but day and month can be mixed.
        :param end_date: pandas Datetime object or a str, if time range from date to end_date should be returned.
        Supported string format for currencies is capital three letter abbreviation (same as source CNB).
        :param date_format: a custom format if the date string is not automatically recognized by parser.
        :param currency: String or a list of strings of currencies to be exported.
        Default None -> all currencies are exported.
        :param filled: bool, default = False.
        If True, returned series will contain all data filled with datapoints from previous valid date.
        """

        date = self._get_valid_date(date=date, date_format=date_format)

        if currency is None:
            currency = self.data.columns

        if end_date is None:
            return self.data.loc[date, currency]
        else:
            end_date = self._get_valid_date(date=end_date)

        if not self.ascend:
            date, end_date = end_date, date

        if filled:
            return self.data.loc[date:end_date, currency].resample('D').ffill()

        return self.data.loc[date:end_date, currency]
