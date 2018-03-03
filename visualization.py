import json
from matplotlib import pyplot as plt
f = open("putuo.txt","r")
position = json.loads(f.read())
f.close()
f = open("position_class.txt","r")
cla = json.loads(f.read())
f.close()
lng = []
lat = []
for bike in position:
    lng.append(bike['lng'])
    lat.append(bike['lat'])


plt.plot(lng,lat)
plt.show()

