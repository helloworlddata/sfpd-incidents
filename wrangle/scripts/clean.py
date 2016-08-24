"""
Renames columns, standardizes data, removes redundancies
"""

import argparse
from csv import DictWriter, DictReader
from datetime import datetime
from loggy import loggy
from sys import stdout

PACIFIC_TZ_SUFFIX = '-0700'

RAW_HEADERS = [
    'IncidntNum','Category','Descript','DayOfWeek','Date','Time',
    'PdDistrict','Resolution','Address','X','Y','Location','PdId',
]

CLEAN_HEADERS = [
    'incident_number', 'datetime',
    'category', 'description', 'resolution',
    'pd_district', 'address',
    'longitude', 'latitude',
    'pd_id',
]

LOGGY = loggy("clean_data")


def clean_row(row):
    """Returns a new dict with clean headers and values"""
    r = {k: v.strip() for k, v in row.items()}
    d = {}
    d['incident_number'] = r['IncidntNum']
    d['category'] = r['Category']
    d['description'] = r['Descript']
    dt = datetime.strptime(r['Date'] + ' ' + r['Time'], '%m/%d/%Y %H:%M')
    d['datetime'] = dt.strftime('%Y-%m-%d %H:%M:%S') + PACIFIC_TZ_SUFFIX
    d['pd_district'] = r['PdDistrict']
    d['resolution'] = r['Resolution']
    d['address'] = r['Address']
    d['longitude'] = r['X']
    d['latitude'] = r['Y']
    d['pd_id'] = r['PdId']
    return d



if __name__ == '__main__':
    parser = argparse.ArgumentParser("Lightly clean and edit the raw SFPD incident data")
    parser.add_argument('infile', type=argparse.FileType('r'), help="Filename or stdin. For the latter, headers won't be echoed to stdout")
    args = parser.parse_args()

    infile = args.infile
    LOGGY.info("Reading from %s" % infile.name)
    csvin = DictReader(infile, fieldnames=RAW_HEADERS)

    csvout = DictWriter(stdout, fieldnames=CLEAN_HEADERS)
    csvout.writeheader()

    for row in csvin:
        if 'IncidntNum' in row.values():
            pass
        else:
            csvout.writerow(clean_row(row))


