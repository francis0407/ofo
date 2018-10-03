import spider
import json

f = open("putuo.txt","r")
position = json.loads(f.read())
f.close()
positions = []
for pos in position:
    positions.append(pos)
    # positions.append({"lng":pos['lng'] + 0.001,"lat":pos['lat']})
    # positions.append({"lng": pos['lng'] + 0.001, "lat": pos['lat'] + 0.001})
    # positions.append({"lng": pos['lng'] , "lat": pos['lat']+ 0.001})

record = []
result = []
total = 0
times = len(positions)

for pos in positions:
    times = times - 1
    info = spider.spider_single(pos['lng'],pos['lat'])
    count = 0
    local = []
    for bike in info['body']['bicycles']:
        posStr = str(bike['longitude'])+str(bike['latitude'])
        if posStr in local:
            result.append(bike)
        if not (posStr in record):
            result.append(bike)
            record.append(posStr)
            count = count + 1
        if not (posStr in local):
            local.append(posStr)



    print("剩余%d个点，本次获取%d，增加%d  重复%d个"%(times,info['body']['total'],count,info['body']['total']-len(local)))

print(len(result))
f = open("positions4.txt","a")
f.write(json.dumps(result))
f.close()
