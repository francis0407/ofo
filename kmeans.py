from sklearn.model_selection import StratifiedKFold
from sklearn import datasets
import random
import numpy as np
import matplotlib.pyplot as plt
import time
import json

# inputs = [[-35,3],[-50,18],[3,0],[5,8],[-14,-5],[-55,10],[-50,5],[-45,-10],[-55,0],[-40,8],[15,8],[15,11],[-40,-2],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],[-49,15],[26,13],[-46,5],[-34,-1],[11,15],[-22,-16],[19,28],[-12,-8],[-13,-19],[-41,11],[-11,-6],[-25,-9],[-18,-3]]
f = open("putuo.txt","r")
position = json.loads(f.read())
inputs = []
for item in position:
    inputs.append(list(item.values()))
inputs = np.array(inputs)
print(inputs)
m = len(inputs)
f.close()
def drawProcess(data,data_class,centers,K,Title):
    color = ["b","g","r","c","m","y","k","w"]
    char = ["x","o","v","<",">"]
    plt.figure("Kmeans")
    plt.title(Title)
    centers_list = centers.tolist()
    for i in range(K):
        class_K =data[data_class == i].T.tolist()
        plt.plot(class_K[0],class_K[1],"%co"%color[i])
        plt.plot([centers_list[i][0]],[centers_list[i][1]],"%c%c"%(color[i],char[i]),label='Class%d'%i,mew="8")
    plt.show()


#计算数据与中心点的距离
def getDistance(data,centers):
    distance = []
    # if centers.shape
    for center in centers:
        # print(center)
        cur_distance = np.sum((data - center)**2 , axis=1) ** 0.5
        try:
            distance = np.vstack((distance,cur_distance))
        except:
            distance = cur_distance
    return distance.T


#选取k个初始点
def setInitialPoint(data,K):
    #随机第一个中心
    random.seed(time.time())
    rand_point_index = int(random.random()*len(data))
    centers = data[rand_point_index].reshape(1,len(data[0]))
    for i in range(1,K):
        distance = getDistance(data,centers)
        try:
            new_center_index = np.argmax(np.min(distance,axis=1))
        except:
            new_center_index = np.argmax(distance)
        centers = np.vstack((centers,data[new_center_index]))
    # print("InitialPoint")
    # print(centers)
    return centers

#获取新的分类
def getClass(data,centers):
    distance = getDistance(data,centers)
    return np.argmin(distance,axis=1)

#改变中心位置
def setNewCenter(data,data_class,K):
    centers = []
    for i in range(K):
        class_K =  data[data_class == i]
        new_center =  np.mean(class_K,axis=0).tolist()
        centers.append(new_center)
    return np.array(centers)
#迭代聚类
def Kmeans(data,K,ifdraw):
    centers = setInitialPoint(data,K)
    data_class = getClass(data,centers)
    if ifdraw:
        drawProcess(data, data_class,centers,K,"Initial Point")
    centers = setNewCenter(data,data_class,K)
    # print(centers)
    new_class = getClass(data,centers)
    if ifdraw:
        drawProcess(data,new_class,centers,K,"ClassChange")
    while not (data_class == new_class).all():
        data_class = new_class
        centers = setNewCenter(data,data_class,K)
        new_class = getClass(data,centers)
        if ifdraw:
            drawProcess(data,new_class,centers,K,"ClassChange")
    if ifdraw:
        drawProcess(data, new_class, centers, K, "FinallStatus")
    return data_class,centers

#计算轮廓系数
def getSilhouetteCoefficient(data,data_class,K):
    S = 0
    for i in range(K):
        class_i = data[data_class == i]
        class_not_i = data[data_class != i]
        # a[i]
        distance = getDistance(class_i,class_i)
        # print(class_i)
        a = np.mean(distance,axis=1)
        # print(a)
        distance = getDistance(class_i,class_not_i)
        b = np.min(distance,axis=1)
        # print(b)
        S = S + np.sum((b-a)/np.max(np.vstack((a,b)),axis=0))
        # print(S)
    return S/len(data)


# max_S = 0
# max_K = 0
# k = []
# s = []
# for i in range(4,4):
#     data_class,centers = Kmeans(inputs,i,ifdraw=0)
#     try:
#         S = getSilhouetteCoefficient(inputs,data_class,i)
#         print("SilhouetteCoefficient:%f  K:%d"%(S,i))
#         if max_S < S:
#             max_S = S
#             max_K = i
#         s.append(S)
#         k.append(i)
#     except:
#         S = 0
# print("Best K:%d"%max_K)
# print(k,s)
# plt.figure("K")
# plt.title("SilhouetteCoefficient for Different K")
# plt.plot(k,s,'')
# plt.xlabel("K")
# plt.ylabel("SilhouetteCoefficient")
# plt.show()
data_class,centers = Kmeans(inputs,400,ifdraw=0)
result = data_class.dumps()
result = data_class.tolist()
f = open("position_class400.txt","w")
f.write(json.dumps(result))
f.close()
# print(getSilhouetteCoefficient(inputs,data_class,3))
# print(getDistance(inputs,np.array([[0,1],[2,3]])))
