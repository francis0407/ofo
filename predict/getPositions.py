import spider
import pymysql
import json
db = pymysql.connect("182.254.209.161","root","123456","ofo",charset="utf8",port=3306)
cursor = db.cursor()

select = "Select lng,lat from putuo_address_info"
positions = []
try:
    cursor.execute(select)
    result = cursor.fetchall()
    for row in result:
        lng = float(row[0])
        lat = float(row[1])
        positions.append({"lng":lng,"lat":lat})
except Exception as e:
    print("a")
    raise e

f = open("putuo.txt","w")
f.write(json.dumps(positions))
f.close()