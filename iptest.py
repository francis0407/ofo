import spider
import threading

def error_handler():
    import time
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("ErrorTime:%s"%(time_string))
    return

def test(i):
    import time
    cur_time = time.time()
    while 1:
        info = spider.spider_single(121.332,31.297,0)
        if info['code']!= 200:
            print(info)
            error_handler()
            break
        else:
            if time.time() - cur_time > 180:
                print("线程%d正常运行： %s"%(i,time.strftime("%H:%M:%S", time.localtime())))
                print(info)
                cur_time = time.time()
    return

def iptest(threadid):
    while 1:
        try_time = time.time()
        lock.acquire()
        global start_time
        if time.time() - start_time>= 600:
            print("Running.. %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            start_time = time.time()
        lock.release()
        while 1:
            try:
                info = spider.spider_single(121.332,31.297,0)
                if info['code']!=200:
                    print(info)
                    print("线程%d退出"%(threadid))
                    error_handler()
                    return
                break
            except:
                curtime = time.time()
                if curtime - try_time <= 120:
                    continue
                else:
                    print("线程%d请求超时，退出"%(threadid))
                    error_handler()
                    return



import time
time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("StartTime:%s"%(time_string))
thread = []
lock = threading.Lock()
start_time = time.time()
for i in range(500):
    thread.append(threading.Thread(target=iptest,args=(i,)))
for i in range(500):
    thread[i].start()
for i in range(500):
    thread[i].join()





