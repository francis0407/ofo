import json
from matplotlib import pyplot as plt
f = open("putuo.txt","r")
position = json.loads(f.read())
f.close()
f = open("position_class400.txt","r")
cla = json.loads(f.read())
f.close()
new_p = []

for i in range(len(position)):
    item = position[i]
    item['class'] = cla[i]
    new_p.append(item)

f = open("position_with_class400.txt","w")
f.write(json.dumps(new_p))
f.close()