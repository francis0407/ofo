import requests
import json
def insertValue(value,string):
    return string+','+"'"+value+"'"
def insertInfo(poi):
    insert = "Insert into bus(id,name,type,typecode,biz_type,address,location,tel,distance,biz_ext,pname,cityname," \
             "adname,importance,shopid,shopinfo,poiweight)" \
             "VALUES "
    value = ''
    for item in poi.values():
        # print(item)
        value = insertValue(str(item),value)
    insert = insert+'('+value[1:]+')'
    # print(insert)
    return insert

url = "http://restapi.amap.com/v3/place/text?key=98ed26568fc668747a1307fc9ff2b1b7&types=150500&city=310107&page="
# text = requests.get(url)
# pois = json.loads(text.text)
# pois = pois['pois']
# insertInfo(pois[0])
import pymysql
db = pymysql.connect("localhost","root","123456","db_busstation",charset="utf8")
cursor = db.cursor()
# insert = "Insert into new_table(id,name)VALUES ('test','test')"
for i in range(1,6):
    url_with_page = url+str(i)
    response = requests.get(url_with_page)
    # print(response.text)
    response = json.loads(response.text)
    pois = response['pois']
    for poi in pois:
        insert = insertInfo(poi)
        try:
            cursor.execute(insert)
            db.commit()
        except:
            db.rollback()
            print("Error")
            print(insert)

    # print(len(pois))

# print(text.text)