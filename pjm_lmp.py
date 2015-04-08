import json
import requests
import sqlite3
import csv
import date_helpers

pnode_list = []

with open("AEP_pnode_list.csv", "r") as fh:
    fh_reader = csv.reader(fh)
    for row in fh_reader:
        pnode_list.append(int(row[0]))

plist1 = pnode_list[0:50]
plist2 = pnode_list[51:100]
plist3 = pnode_list[101:150]
plist4 = pnode_list[151:200]
plist5 = pnode_list[201:250]
plist6 = pnode_list[251:300]
plist7 = pnode_list[301:350]
plist8 = pnode_list[351:400]
plist9 = pnode_list[401:450]
plist10 = pnode_list[451:500]
plist11 = pnode_list[501:550]
plist12 = pnode_list[551:600]
plist13 = pnode_list[600:]


data = {"startDate": "2011-01-01", "endDate": "2014-04-08", "pnodeList": plist5}
data = json.dumps(data)

url = 'https://dataminer.pjm.com/dataminer/rest/public/api/markets/realtime/lmp/daily'

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=data, headers=headers)

print(response.status_code)
result_json = response.json()
print("")

# TODO: create a separate script the puts together the pNode list, and calls this script to call API


# Create a table with same headers as the CSV export from the GUI-based DataMiner
with sqlite3.connect("pjm_lmp.db") as connection:
    c = connection.cursor()
    c.executescript("""
    DROP TABLE IF EXISTS LMP;
    CREATE TABLE LMP(PublishDate TEXT, Version TEXT,
                        PnodeID TEXT, PricingType TEXT,
                        H1 REAL, H2 REAL, H3 REAL, H4 REAL,
                        H5 REAL, H6 REAL, H7 REAL, H8 REAL,
                        H9 REAL, H10 REAL, H11 REAL, H12 REAL,
                        H13 REAL, H14 REAL, H15 REAL, H16 REAL,
                        H17 REAL, H18 REAL, H19 REAL, H20 REAL,
                        H21 REAL, H22 REAL, H23 REAL, H24 REAL);
    """)

    bulk_data = []
    json_transform = {}

    for record in result_json:

        if record['priceType'] == 'TotalLMP':
            json_transform['publishDate'] = date_helpers.UTC_to_date_string(record['publishDate'])
            json_transform['pnodeId'] = record['pnodeId']
            json_transform['priceType'] = record['priceType']
            json_transform['versionNum'] = record['versionNum']

            for price in record['prices']:
                new_hour = date_helpers.UTC_to_local_hour(price['utchour'])
                json_transform['H{}'.format(new_hour)] = price['price']

            if 'H3' in json_transform:
                pass
            else:
                json_transform['H3'] = 0

            row_data = (json_transform['publishDate'], json_transform['versionNum'], json_transform['pnodeId'],
                          json_transform['priceType'],
                          json_transform['H1'],
                          json_transform['H2'],
                          json_transform['H3'],
                          json_transform['H4'],
                          json_transform['H5'],
                          json_transform['H6'],
                          json_transform['H7'],
                          json_transform['H8'],
                          json_transform['H9'],
                          json_transform['H10'],
                          json_transform['H11'],
                          json_transform['H12'],
                          json_transform['H13'],
                          json_transform['H14'],
                          json_transform['H15'],
                          json_transform['H16'],
                          json_transform['H17'],
                          json_transform['H18'],
                          json_transform['H19'],
                          json_transform['H20'],
                          json_transform['H21'],
                          json_transform['H22'],
                          json_transform['H23'],
                          json_transform['H24'])

            bulk_data.append(row_data)

    c.executemany("""INSERT INTO LMP (PublishDate, Version, PnodeID, PricingType,
                                    H1, H2, H3, H4,
                                    H5, H6, H7, H8,
                                    H9, H10, H11, H12,
                                    H13, H14, H15, H16,
                                    H17, H18, H19, H20,
                                    H21, H22, H23, H24)

                                    VALUES(?, ?, ?, ?,
                                            ?, ?, ?, ?,
                                            ?, ?, ?, ?,
                                            ?, ?, ?, ?,
                                            ?, ?, ?, ?,
                                            ?, ?, ?, ?,
                                            ?, ?, ?, ?)""", bulk_data)
