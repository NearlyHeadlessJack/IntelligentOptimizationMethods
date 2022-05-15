import numpy as np
from data import Data
from savedata import SaveData

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
        # print(self.data.now)
        # print(self.data.now_result)
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
        self.data.reset()
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
        # print(self.data.best)
        # print(self.data.best_result)
        return self.data.best_result
        
        
    def exp1(self):
        save = SaveData()
        temp01 = 300
        temp1 = 800
        deltaT1 = 10
        inner_count1 = 5
        
        temp02 = 300
        temp2 = 800
        deltaT2 = 10
        inner_count2 = 20
        
        temp03 = 300
        temp3 = 800
        deltaT3 = 10
        inner_count3 = 80
        
        temp04 = 300
        temp4 = 800
        deltaT4 = 10
        inner_count4 = 200
        
        for i in range(500):
            self.data = Data()
            best = self.search(temp0=temp01,temp=temp1,r=0.97,deltaT=deltaT1,isDelta=True,inner_count=inner_count1)
            save.save(i,temp01,temp1,deltaT1,inner_count1,best)
            best = self.search(temp0=temp02,temp=temp2,r=0.97,deltaT=deltaT2,isDelta=True,inner_count=inner_count2)
            save.save(i,temp02,temp2,deltaT2,inner_count2,best)
            best = self.search(temp0=temp03,temp=temp3,r=0.97,deltaT=deltaT3,isDelta=True,inner_count=inner_count3)
            save.save(i,temp03,temp3,deltaT3,inner_count3,best)
            best = self.search(temp0=temp04,temp=temp4,r=0.97,deltaT=deltaT4,isDelta=True,inner_count=inner_count4)
            save.save(i,temp04,temp4,deltaT4,inner_count4,best)
            del self.data
            
            
        save.write_data()
        
        
    def exp2(self):
        save = SaveData()
        temp01 = 300
        temp1 = 400
        deltaT1 = 3
        inner_count1 = 5
        
        temp02 = 300
        temp2 = 600
        deltaT2 = 3
        inner_count2 = 20
        
        temp03 = 300
        temp3 = 800
        deltaT3 = 3
        inner_count3 = 80
        
        temp04 = 300
        temp4 = 1000
        deltaT4 = 3
        inner_count4 = 200
        
        for i in range(500):
            self.data = Data()
            best = self.search(temp0=temp01,temp=temp1,r=0.97,deltaT=deltaT1,isDelta=True,inner_count=inner_count1)
            save.save(i,temp01,temp1,deltaT1,inner_count1,best)
            best = self.search(temp0=temp02,temp=temp2,r=0.97,deltaT=deltaT2,isDelta=True,inner_count=inner_count2)
            save.save(i,temp02,temp2,deltaT2,inner_count2,best)
            best = self.search(temp0=temp03,temp=temp3,r=0.97,deltaT=deltaT3,isDelta=True,inner_count=inner_count3)
            save.save(i,temp03,temp3,deltaT3,inner_count3,best)
            best = self.search(temp0=temp04,temp=temp4,r=0.97,deltaT=deltaT4,isDelta=True,inner_count=inner_count4)
            save.save(i,temp04,temp4,deltaT4,inner_count4,best)
            del self.data
            
            
        save.write_data()
            
            

                
            
            
            
        