"""
Removes unnecessary columns
"""

from pathlib import Path
from csv import DictWriter, DictReader
from datetime import datetime

HEADERS = [
    'incident_num', 'category', 'description',
    'datetime', 'pd_district', 'resolution',
    'day_of_week', 'address', 'longitude', 'latitude',
    'pd_id'
]

SRC_PATH = Path('wrangle', 'corral', 'fetched', 'sfpd-incidents_tmnf-yvry.csv')
DEST_PATH = Path('wrangle', 'corral', 'cleaned', 'sfpd-incidents.csv')
DEST_PATH.parent.mkdir(exist_ok=True, parents=True)

srcfile = SRC_PATH.open('r')
srccsv = DictReader(srcfile)

destfile = DEST_PATH.open('w')
destcsv = DictWriter(destfile, fieldnames=HEADERS)
destcsv.writeheader()

for i, r in enumerate(srccsv):
    d = {}
    d['incident_num'] = r['IncidntNum']
    d['category'] = r['Category']
    d['description'] = r['Descript']
    d['datetime'] = datetime.strptime(r['Date'] + r['Time'], '%m/%d/%Y%H:%M')
    d['day_of_week'] = r['DayOfWeek'][0:3]
    d['pd_district'] = r['PdDistrict']
    d['resolution'] = r['Resolution']
    d['address'] = r['Address']
    d['longitude'] = r['X']
    d['latitude'] = r['Y']
    d['pd_id'] = r['PdId']
    destcsv.writerow(d)
    if i % 10000 == 1:
        print("Wrote row:", i)

srcfile.close()
destfile.close()

