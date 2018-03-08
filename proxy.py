import requests
import time
import random
proxy_list = [0]
updateTime = 0
def getNewProxyList():
    # global  updateTime
    # curtime = time.time()
    # if updateTime != 0 or curtime - updateTime <= 8:
    #     return [0]
    # updateTime = curtime
    # result = requests.get("http://dev.kuaidaili.com/api/getproxy/?orderid=931997361484873&num=50&area=%E4%B8%8A%E6%B5%B7&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_an=1&an_ha=1&sp1=1&sep=2")
    # proxy = result.text
    # new_list = proxy.split('\n')
    # if proxy.find("ERROR")!=-1:
    #     return [0]
    # return new_list

    # 不获取代理
    return [0]

def mergeProxyList(oldlist,newlist):
    templist = list(set(oldlist+newlist))
    return  templist

def testProxy(proxy):
    # import spider
    # try:
    #     spider.spider_single(121.372,31.271,proxy)
    # except:
    #     return 0
    # return 1
    return 1

def getProxy():
    # global proxy_list
    # if len(proxy_list) < 3:
    #     try:
    #         new_list = getNewProxyList()
    #     except:
    #         print("代理池获取失败")
    #         return 0
    #     new_list = mergeProxyList(proxy_list,new_list)
    #     valid_list = []
    #     for proxy in new_list:
    #         if testProxy(proxy):
    #             valid_list.append(proxy)
    #     proxy_list = valid_list
    #     print("代理池获取成功，剩余代理个数 %d"%(len(proxy_list)))
    # if not len(proxy_list):
    #     print("无有效代理")
    #     raise Exception("无有效代理")
    #     return 0
    # else:
    #     proxy = proxy_list[int(random.random()*len(proxy_list))]
    #     # print(proxy)
    #     return proxy
    return 0

def updateProxy():
    # global proxy_list
    # valid_list = []
    # for proxy in proxy_list:
    #     if testProxy(proxy):
    #         valid_list.append(proxy)
    # proxy_list = valid_list
    # print("代理池更新成功，剩余代理个数 %d" % (len(proxy_list)))
    return
def deleteProxy(ip):
    # global proxy_list
    # if ip in proxy_list:
    #     proxy_list.remove(ip)
    #     print("%s失效"%(str(ip)))
    return