import threading
import spider
import proxy
import json
import time
lock = threading.Lock()
history = []
result = []
total_point = 0
def spider_with_class(cls,position,ip=0,date="ofo_temp"):
    mypos = []

    for item in position:
        if item['class'] == cls:
            mypos.append(item)
            mypos.append({"lng":item['lng'] + 0.005,"lat":item['lat']})
            mypos.append({"lng": item['lng'] + 0.005, "lat": item['lat'] + 0.005})
            mypos.append({"lng": item['lng'] , "lat": item['lat']+ 0.005})
    # print("线程%d  共%d个原始点"%(cls,len(mypos)))
    #
    global history
    # record = []

    ip = proxy.getProxy()

    i = len(mypos)
    for pos in mypos:
        i = i - 1
        count = 0
        local = []
        localString = []
        info = 0
        try:
            info = spider.spider_single(pos['lng'],pos['lat'],ip)
        except:
            if not proxy.testProxy(ip):
                proxy.deleteProxy(ip)
            ip = proxy.getProxy()
            try:
                info = spider.spider_single(pos['lng'],pos['lat'],ip)
            except:
                proxy.updateProxy()
                ip = proxy.getProxy()
                try:
                    info = spider.spider_single(pos['lng'], pos['lat'], ip)
                except:
                    print("线程%d因网络问题退出 时间:"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                    raise Exception
                    return 0

        lock.acquire()
        for bike in info['body']['bicycles']:
            posStr = str(bike['longitude']) + str(bike['latitude'])
            if not (posStr in history):
                result.append(bike)
                local.append(bike)
                count +=1
                if not (posStr in localString):
                    localString.append(posStr)
        history.extend(localString)
        global total_point
        total_point -= 1
        if total_point % 4000 == 0:
            print("%s 本次剩余%d个"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),total_point))
        lock.release()
        if not save_in_db(local,date):
            while not save_in_db(local,date):
                print("线程%d 数据库连接失败"%(cls))
            # save_in_db(local)
        # print("线程%d 剩余%d次 获取%d个 保存%d个"%(cls,i,info['body']['total'],count))
    # lock.acquire()
    # result.extend(record)
    # lock.release()
    return

def save_record(s,f,d,total,ss,fs):
    import pymysql
    try:
        db = pymysql.connect("182.254.209.161", "root", "123456", "db_ofo", charset="utf8", port=3306)
        cursor = db.cursor()
        insert = "Insert into ofo_record_stable (start_time,finish_time,total,date,start_time_stamp,finish_time_stamp)VALUES('%s','%s',%d,'%s',%s,%s)"%(s,f,total,d,str(ss),str(fs))
        cursor.execute(insert)
        db.commit()
    except:
        db.rollback()
        print("Record Error")
def save_in_db(bikes,date):
    import pymysql
    db = 0
    try:
        db = pymysql.connect("182.254.209.161","root","123456","db_ofo",charset="utf8",port=3306)
        cursor = db.cursor()
    except:
        # print("数据库连接失败")
        return 0
    # global result
    for item in bikes:
        insert = spider.BikeInsertString(item,date)
        try:
            cursor.execute(insert)
            db.commit()
        except:
            db.rollback()
            print("DB Error")
    db.close()
    return 1


f = open("position_with_class100.txt","r")
position = json.loads(f.read())
f.close()
# thread = []
#
# time_string = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
# print("开始时间:%s"%(time_string))
# # print()
# for i in range(400):
#     thread.append(threading.Thread(target=spider_with_class,args=(i,position,0)))
#
# for i in range(400):
#     thread[i].setDaemon(True)
#     thread[i].start()
#
# for i in range(400):
#     thread[i].join()


# time_string = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
# print("全部完成 共获取%d个"%(len(result)))
# print("结束时间:%s"%(time_string))
# f = open("thread_test100.txt","w")
# f.write(json.dumps(result))
# f.close()

# while 1:
#     if time.strftime("%H:%M",time.localtime()) == "00:00":
#         break

while 1:
    date = time.strftime("%Y-%m-%d",time.localtime())

    start_time = time.time()
    print("开始新的查询 当前时间:%s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    start_time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    proxy.getProxy()

    thread = []
    history = []
    result = []
    total_point = len(position) * 4
    for i in range(100):
        thread.append(threading.Thread(target=spider_with_class, args=(i, position, 0,date)))
    for i in range(100):
        thread[i].setDaemon(True)
        thread[i].start()
    for i in range(100):
        thread[i].join()

    # save_in_db()
    cur_time = time.time()
    print("完成一次查询 当前时间:%s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    print("本次共获取 %d 个"%(len(result)))
    finish_time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    save_record(start_time_string,finish_time_string,date,len(result),start_time,cur_time)
    while cur_time - start_time <= 1200:
        time.sleep(10)
        cur_time = time.time()

input()