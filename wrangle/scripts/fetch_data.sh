mkdir -p wrangle/corral/fetched
curl -L 'https://data.sfgov.org/api/views/tmnf-yvry/rows.csv?accessType=DOWNLOAD' \
    -o wrangle/corral/fetched/sfpd-incidents_tmnf-yvry.csv

