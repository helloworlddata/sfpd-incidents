"""
Renames columns, standardizes data
"""

import argparse
from csv import DictWriter, DictReader
from datetime import datetime
from loggy import loggy
from sys import stdout

RAW_HEADERS = [
    'IncidntNum','Category','Descript','DayOfWeek','Date','Time',
    'PdDistrict','Resolution','Address','X','Y','Location','PdId',
]

CLEAN_HEADERS = [
    'incident_num', 'category', 'description',
    'datetime', 'pd_district', 'resolution',
    'day_of_week', 'address', 'longitude', 'latitude',
    'pd_id'
]

LOGGY = loggy("clean_data")


def clean_row(r):
    """Returns a new dict with clean headers and values"""
    d = {}
    d['incident_num'] = r['IncidntNum']
    d['category'] = r['Category']
    d['description'] = r['Descript']
#    LOGGY.info(r['Date'] + ' ' + r['Time'])
    d['datetime'] = datetime.strptime(r['Date'] + ' ' + r['Time'], '%m/%d/%Y %H:%M')
    d['day_of_week'] = r['DayOfWeek'][0:3]
    d['pd_district'] = r['PdDistrict']
    d['resolution'] = r['Resolution']
    d['address'] = r['Address']
    d['longitude'] = r['X']
    d['latitude'] = r['Y']
    d['pd_id'] = r['PdId']
    return d



if __name__ == '__main__':
    parser = argparse.ArgumentParser("Lightly edit the raw SFPD incident data")
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


