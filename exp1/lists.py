'''
搜索产生的各种表的集合及其封装
'''
from ast import Sub
from time import sleep
from types import new_class
import numpy as np
import random


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
        
    def __del__(self):
        self.list = []
        

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
    
    
class Subset:
    set = []
    
    def __init__(self,mov,size):
        change_set = []
        move_set = []
        result_set = []
        self.set.append(change_set)
        self.set.append(move_set)
        self.set.append(result_set)
        
        
        
        i = 0
        for i in range(0,size):
            
            a,b = self.random_generate()
            new_set = {a,b}
            count = 0
            while new_set in self.set[0]:
                count +=1
                a,b = self.random_generate()
                new_set = {a,b}
                if count>20:
                    break
            # print("size")
            # print(i)
            self.set[0].append(new_set)
            self.set[1].append(self.move_change(mov,a,b))
            
    def __del__(self):
        return
        
    def clean(self):
        self.set = []
            
        
        
    def random_generate(self):
        a = np.random.randint(1,101,1)
        b = np.random.randint(1,101,1)
        while(b==a):
            b = np.random.randint(1,101,1)
        return int(a),int(b)
    
    
    def move_change(self,mov,a,b):
        c= mov[a-1]
        mov[a-1] = mov[b-1]
        mov[b-1] = c
        return mov
        
# move = [49, 65, 63, 41, 13, 96, 6, 11, 59, 27, 14, 100, 44, 42, 54, 98, 73, 84, 75, 36, 34, 99, 58, 30, 82, 21, 80, 53, 31, 71, 57, 56, 38, 43, 94, 50, 78, 19, 66, 28, 61, 22, 2, 46, 45, 32, 85, 83, 72, 23, 95, 90, 81, 68, 67, 1, 70, 48, 87, 93, 40, 91, 29, 24, 17, 8, 3, 18, 15, 74, 69, 64, 9, 26, 77, 51, 10, 79, 60, 88, 47, 5, 89, 20, 25, 35, 7, 76, 12, 97, 52, 55, 33, 39, 86, 16, 37, 4, 62, 92]
# test = Subset(move,1)
# print(test.set[1])