__all__ = ['Rates']

from .Rates import Rates

"""The Rates class downloads official exchange rates from the website of Czech National Bank for given year(s).

The possible time range to extract the data is from 1991 (including) until the current year.
The class provides methods to extrack rates for specific currencies or a specific time range. It can handle missing data by taking
the closest previous exchange rate, which is considered to be a valid exchange rate for weekends and holidays when 
the national bank does not publish new data.

The class does not implement other functionalities like loading to and from database. For the most part, expirienced users will use it
only to scrape the data and save them in csv format."""
