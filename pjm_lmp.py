import json
import requests
import sqlite3
import csv

pnode_list = []

with open("AEP_pnode_list.csv", "r") as fh:
    fh_reader = csv.reader(fh)
    for row in fh_reader:
        pnode_list.append(int(row[0]))

plist1 = pnode_list[0:50]
plist2 = pnode_list[51:200]
plist3 = pnode_list[201:400]
plist4 = pnode_list[401:]

data = {"startDate": "2011-04-01", "endDate": "2014-04-02", "pnodeList": [5021072]}
data = json.dumps(data)

url = 'https://dataminer.pjm.com/dataminer/rest/public/api/markets/realtime/lmp/daily'

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=data, headers=headers)

print(response.status_code)
result_json = response.json()
print("")

# TODO: implement daylight savings logic
# Mar: UTC5 - UCT3
# Mar - Nov: UTC4 = UTC3
# Nov: UTC4 - UTC4A
# Nov - Mar: UTC5 - UTC4

# TODO: create a separate script the puts together the pNode list, and calls this script to call API

UTC_to_PJM = {
    '04': 'H1',
    '05': 'H2',
    '06': 'H3',
    '07': 'H4',
    '08': 'H5',
    '09': 'H6',
    '10': 'H7',
    '11': 'H8',
    '12': 'H9',
    '13': 'H10',
    '14': 'H11',
    '15': 'H12',
    '16': 'H13',
    '17': 'H14',
    '18': 'H15',
    '19': 'H16',
    '20': 'H17',
    '21': 'H18',
    '22': 'H19',
    '23': 'H20',
    '00': 'H21',
    '01': 'H22',
    '02': 'H23',
    '03': 'H24',
}


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

    json_transform = {}

    for record in result_json:
        if record['priceType'] == 'TotalLMP':
            json_transform['publishDate'] = record['publishDate'][:10]
            json_transform['pnodeId'] = record['pnodeId']
            json_transform['priceType'] = record['priceType']
            json_transform['versionNum'] = record['versionNum']

            for price in record['prices']:
                new_hour = UTC_to_PJM[price['utchour'][11:13]]
                json_transform[new_hour] = price['price']
            table_data = (json_transform['publishDate'], json_transform['versionNum'], json_transform['pnodeId'],
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

            c.execute("""INSERT INTO LMP (PublishDate, Version, PnodeID, PricingType,
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
                                                    ?, ?, ?, ?)""", table_data)
