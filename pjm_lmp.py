import json
import requests
import sqlite3

data = {"startDate": "2015-04-01", "endDate": "2015-04-01", "pnodeList": [5021072]}
data = json.dumps(data)

url = 'https://dataminer.pjm.com/dataminer/rest/public/api/markets/realtime/lmp/daily'

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=data, headers=headers)

print(response.status_code)
result_json = response.json()
print(result_json)
print("")

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
    json_transform['publishDate'] = record['publishDate']
    json_transform['pnodeId'] = record['pnodeId']
    json_transform['priceType'] = record['priceType']

    for price in record['prices']:
        json_transform[price['utchour']] = price['price']
    print(json_transform)

