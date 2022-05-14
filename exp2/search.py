import numpy as np
from data import Data

"""
搜索算法
"""

class Search:
    def __init__(self,temp0=300,temp=1000,r=0.97,deltaT=10,isDelta=True,inner_count=3) :
        # 初始温度
        self.temp = temp
        # 温度阈值
        self.temp0 = temp0
        # 降温系数
        self.r = r
        # 降温差值
        self.deltaT = deltaT
        # 使用哪种降温方式
        self.isDelta = isDelta
        self.data = Data()
        self.inner_count = inner_count
        
    
    def decrease_temp(self):
        if self.isDelta:
            self.temp -= self.deltaT
        else:
            self.temp *= self.r
    
    
    def isTempDone(self):
        if self.temp <= self.temp0:
            return True
        else:
            return False
        
        
    def cal_and_decide(self,delta):
        exponent = -1.0 * (delta/self.temp)
        bolzman = np.exp(exponent)
        ksai = np.random.uniform(low=0.0, high=1.0)
        if bolzman>ksai:
            return True
        else:
            return False
        
        
    def search_once(self):
        
        old_result = self.data.calculate(self.data.now)
        self.data.random_change()
        new_result = self.data.calculate(self.data.temp)
        delta_result = new_result - old_result
        
        if delta_result<0:
            self.data.now = self.data.temp
            if new_result<self.data.best_result:
                self.data.update_best()
        else:
            if self.cal_and_decide(delta_result):
                self.data.now = self.data.temp
            
    
    
    def search(self,temp0=300,temp=1000,r=0.97,deltaT=10,isDelta=True,inner_count=3):
        # 初始温度
        self.temp = temp
        # 温度阈值
        self.temp0 = temp0
        # 降温系数
        self.r = r
        # 降温差值
        self.deltaT = deltaT
        # 使用哪种降温方式
        self.isDelta = isDelta
        # 内循环次数
        self.inner_count = inner_count

        while not self.isTempDone():
            for i in range(self.inner_count):
                self.search_once()
            self.decrease_temp()
        print(self.data.best)
        print(self.data.best_result)

                
            
            
            
        