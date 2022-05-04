'''
搜索产生的各种表的集合及其封装
'''
from time import sleep
import numpy as np


# 禁忌表类的实现 ========================
class TList:
    list = []
    max_length = 3  # 禁忌表长度
    
    def __init__(self,length):
        self.list=[]
        for i in range(0,length):
            self.list.append({0,0})
        self.max_length = length
        return
    
    def change_size(self,length):
        self.list=[]
        for i in range(0,length):
            self.list.append({0,0})
        self.max_length = length
        return
        
    
    def search(self,obj):
        for list in self.list:
            if(list == obj):
                return True
        return False

    def iter(self,obj):
        for i in range(1,self.max_length):
            self.list[self.max_length-i] = self.list[self.max_length-i-1]
        self.list[0] = obj

# test = TList(3)
# test.iter({1,2})
# test.iter({1,3})
# test.iter({1,4})
# test.iter({1,5})
# print(test.search({1,4}))
# 频数表类的实现 ========================

class PList:
    best = 0 # 渴望水平
    map = [[],[]]
    
    def __init__(self):
        self.map = [[],[]]
        return
    
    def iter(self,obj,isBan=False):
        if isBan:
            return 0
        for set in self.map[0]:
            if set == obj:
                return self.map[0].index(set)
        return 0
                    

    
    def add(self,obj):
        index = self.iter(obj)
        if index == 0:
            self.map[0].append(obj)
            self.map[1].append(1)
        else:
            self.map[1][index] += 1
            
class Cache:
    
    r = []
    m1 = []
    m2 = []
    
    
    def __init__(self):
        self.r=np.array(self.r)
        self.m1=np.array(self.m1)
        self.m2=np.array(self.m2)
        
    def add(self,m1,m2,r):
        self.r=np.append(self.r,r)
        self.m1=np.append(self.m1,m1)
        self.m2=np.append(self.m2,m2)
        
    def minimum(self):
        minr = float(np.min(self.r))
        index = np.where(self.r == np.min(self.r))

        return minr,int(self.m1[index]),int(self.m2[index])