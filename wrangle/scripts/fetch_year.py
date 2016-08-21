"""
python fetch_year.py 2012 > 2012.csv


This script is overly complicated because we want to idempotenly
fetch data, year by year. The Socrata API does not allow for more than
50,000 records to be fetched in a single call. Furthermore, it
won't let us sort by two different fields (`Date` and `Time`) so we
have to perform that manually, in-memory, at the end, before outputting
to stdout
"""

from copy import copy
from csv import DictReader, DictWriter
from loggy import loggy
from sys import stdout
import argparse
import requests

myloggy = loggy('fetch_year.py')

MAX_LIMIT = 50000

BASE_SRC_URL = "https://data.sfgov.org/resource/tmnf-yvry.csv"
DEFAULT_PARMS = {
    '$limit': MAX_LIMIT,
    '$order': ':id',
    '$offset': 0,
}

def query_year(year, offset):
    parms = copy(DEFAULT_PARMS)
    parms['$offset'] = offset
    parms['$where'] = "date > '{0}' and date < '{1}'".format(year, year+1)
    resp = requests.get(BASE_SRC_URL, params=parms)
    return resp

def fetch_full_year(year):
    offset = 0
    all_lines = []

    while True:
        resp = query_year(year, offset)
        txt = resp.text
        lines = txt.splitlines()

        myloggy.info(resp.url)
        myloggy.info("\tOffset: %s" % offset)
        myloggy.info("\tLines received (+ header): %s" % len(lines))

        if not all_lines: # need to include header
            all_lines.extend(lines)
        else:
            all_lines.extend(lines[1:])

        if len(lines) < MAX_LIMIT + 1:
            myloggy.info("\tBreaking loop; %s lines received is less than limit of %s" % (len(lines), MAX_LIMIT + 1))
            break
        else:
            offset += MAX_LIMIT

    myloggy.info("Total lines (+ header): %s" % len(all_lines))
    return DictReader(all_lines)





if __name__ == '__main__':
    parser = argparse.ArgumentParser("Download data from %s by year" % BASE_SRC_URL)
    parser.add_argument('year', type=int)
    args = parser.parse_args()
    year = args.year
    csvin = fetch_full_year(year)
    csvout = DictWriter(stdout, fieldnames=csvin.fieldnames)
    csvout.writeheader()
    for row in sorted(csvin, key=lambda r: (r['Date'], r['Time'])):
        csvout.writerow(row)


