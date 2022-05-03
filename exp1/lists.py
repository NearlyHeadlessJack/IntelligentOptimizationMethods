'''
搜索产生的各种表的集合及其封装
'''
from time import sleep


# 禁忌表类的实现 ========================
class TList:
    
    list = []
    max_length = 3  # 禁忌表长度
    
    def __init__(self,length):
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


# 频数表类的实现 ========================

class PList:

    map = [[],[]]
    
    def __init__(self):
        return
    
    def iter(self,obj):
        for set in self.map[0]:
            if set == obj:
                return self.map[0].index(set)
        return -1
                    
        
    def add(self,obj):
        index = self.iter(obj)
        if index == -1:
            self.map[0].append(obj)
            self.map[1].append(1)
        else:
            self.map[1][index] += 1