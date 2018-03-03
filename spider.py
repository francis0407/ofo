import requests
import json
import pymysql
import time
def spider_single(lon,lat,proxy = 0):

    url ='https://api.open.ofo.com/v1/near/bicycle'
    headers = {
        'Host': 'api.open.ofo.com',
        'Content - Type': 'application / json',
        'Accept': '* / *',
        'Accept - Encoding': 'gzip, deflate',
        'Connection': 'keep - alive',
        'Pragma': 'no - cache',
        'User - Agent': 'OneTravel/5.1.8 (iPhone; iOS 10.3.3; Scale/2.00)',
        'Accept - Language': 'zh - Hans - CN;q = 1',
        'Cache - Control': 'no - cache'
    }
    values={"appKey":"didi","number":"50","longitude":lon,"radius":"200","mapType":"1","latitude":lat,"datatype":"101","appversion":"5.1.8"}
    result = 0
    proxies = {"http":proxy,"https":proxy}
    if proxy != 0:
        result = requests.post(url = url,headers = headers,data=values)
    else:
        result = requests.post(url = url,headers = headers,data=values,proxies = proxies)
    info = json.loads(result.text)
    # print(info)
    return info

def getNos(info):
    bicycles = info['body']['bicycles']
    bic_list = []
    for bic in bicycles:
        bic_list.append(bic['bicycleNo'])
    return bic_list

def mergeNos(old_list,new_list):
    final_list = list(set(old_list+new_list))
    # print("添加 %d"%(len(final_list)-len(old_list)))
    return final_list,(len(final_list)-len(old_list))

def getMaxMinLon_Lat(info):
    bicycles = info['body']['bicycles']
    lon_list = []
    lat_list = []
    for bic in bicycles:
        lon_list.append(bic['longitude'])
        lat_list.append(bic['latitude'])
    return max(lon_list),min(lon_list),max(lat_list),min(lat_list)
# No_list = []
# # for i in range(5):
# #     info = spider_single(121.365768,31.297934)
# #     new_list = getNos(info)
# #     No_list,diff = mergeNos(No_list,new_list)
# diff = 100
# i = 0
# max_lon = 0
# max_lat = 0
# min_lon = 1000
# min_lat = 1000
def BikeInsertString(bic):
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    insert = "Insert into 2018_3_2(lng,lat,time)VALUES (%s,%s,'%s')"%(str(bic['longitude']),str(bic['latitude']),time_string)
    # print
    return insert

#数据库存储
# db = pymysql.connect("182.254.209.161","root","123456","db_ofo",charset="utf8",port=3306)
# cursor = db.cursor()
# No_list = []
# diff = 100
# i = 0
# while diff != 0:
#     i = i+1
#     info = spider_single(121.365768,31.297934)
#     new_list = getNos(info)
#     No_list,diff = mergeNos(No_list,new_list)
#     print("第%d次 获得%d个 新增%d个" % (i, info['body']['total'],diff))
#     for bic in info['body']['bicycles'] :
#         insert = saveBicInsertString(bic)
#         # print(insert)
#         try:
#             cursor.execute(insert)
#             db.commit()
#         except:
#             db.rollback()
#             print("Error")





#121.365768,31.297934 121.456892,31.297934
#121.365768,31.229408 121.456892,31.229408

#临时获取
# result = []
# Nos = []
# for i in range(2):
#     info = spider_single(121.403571,31.227633)
#     for bic in info['body']['bicycles']:
#         pos = {"lng":bic['longitude'],"lat":bic['latitude'],'count':1}
#         result.append(pos)
#     new_No = getNos(info)
#
#     print("第%d次获取，获得%d个"%(i,info['body']['total']))


# f = open("positions2.txt","a+")
# f.write(json.dumps(result))
# f.close()




