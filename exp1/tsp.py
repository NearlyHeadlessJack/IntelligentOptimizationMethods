'''
TSP Benchmark问题求解
使用数据KroA100
初始解随机产生
领域移动方式为2-opt
采用基于概率的邻域搜索方式
惩罚因子设为0.001
采用t-检验的方式分析算法性能
'''
from cgitb import reset
from dataloader import Dataloder
from lists import TList, PList,Cache,Subset
import random,math
from savedata import SaveData
import numpy as np
import time


def init():
    list = d.city_name
    random.shuffle(list)
    return list
    
def cal(mov):
    dis = 0
    for i in range(1,100):
        index = int(mov[i]) - 1
        index_pev = int(mov[i-1]) - 1
        dis += math.sqrt((d.city_location[index][0] - d.city_location[index_pev][0]) ** 2 + (d.city_location[index][1] - d.city_location[index_pev][1]) ** 2)    
    index = int(mov[0]) - 1
    index_pev = int(mov[99]) - 1
    dis += math.sqrt((d.city_location[index][0] - d.city_location[index_pev][0]) ** 2 + (d.city_location[index][1] - d.city_location[index_pev][1]) ** 2)
    return dis

def randmov():
    a = random.randint(1,100)
    b = random.randint(1,100)
    while(b==a):
        b = random.randint(1,100)
    return a,b

def mov(mov,move):
    mov = list(mov)
    c = move[mov[0]-1]
    move[mov[0]-1] = move[mov[1]-1]
    move[mov[1]-1] = c
    return move
    

class Search:
    
    r_now_result = 0
    r_total = 0
    
    subset =[]
    def __init__(self,movee,epochs,alpha,tlist_size=20,sub_size=100,isBan=False):
        mov = movee
        optimum_result = cal(mov)
        now_result = cal(mov)
        p = PList()
        t = TList(tlist_size)
        total = 0
        epoch = 0
        self.subset = Subset(mov,sub_size)
        self.subset.shuffle(mov,sub_size)
        print(self.subset.set[0])
        while epoch<epochs:
            total += 1
            epoch += 1
            # if epoch == 1:
            #     self.subset.shuffle(mov,sub_size)
            i = 0
            
            for i in range(0,sub_size):
                p.add(self.subset.set[0][i])
                self.subset.iter(i)
                result = cal(self.subset.set[1][i]) + alpha * p.iter(self.subset.set[0][i],isBan)
                self.subset.set[2][i] = result
            distances = self.subset.set[2]
            distances = np.array(distances)

            index_of_order = np.argsort(distances)
            # print(index_of_order)
            j = 0 
            _dis = self.subset.set[2][index_of_order[0]]
            # if _dis>now_result:
            #     self.r_now_result = optimum_result
            #     self.r_total = total
                # return
            for j in range(0,sub_size):

                # print(epoch)
                # print(subset.set)
                ordered_index = index_of_order[j]
                _set = self.subset.set[0][ordered_index]
                _move = self.subset.set[1][ordered_index]
                _dis = self.subset.set[2][ordered_index]
                isInTlist = t.search(_set)
                print(isInTlist)
                print('j:')
                print(j)
                
                    
                if not isInTlist:
                
                    t.iter(_set)
                    now_result = _dis
                    if now_result<optimum_result:
                        optimum_result = now_result
                    mov = _move
                    break
                else:
                    
                    if _dis<optimum_result:
                        t.iter(_set)
                        now_result = _dis
                        optimum_result = now_result
                        mov = _move
                        break
                    else:
                        continue
            print(t.list)
            # self.subset.clean()
            # del ssubset
            if total>200:
                print('break')
                print(now_result)
                self.r_now_result = now_result
                self.r_total = total
                return
                
        del p
        del t
        # print(mov)
        print("\n")
        self.r_now_result = optimum_result
        self.r_total = total
        return
    def __del__(self):
        return

            
        
    
if __name__ == "__main__":
    
    a = 0.001
    epo = 10000
    ts = 300
    
    ss = 400
    # iB = True
    d = Dataloder()
    s = SaveData()
    
    # move = init()
    move =[49, 65, 63, 41, 13, 96, 6, 11, 59, 27, 14,100, 44, 42, 54, 98, 73, 84, 75, 36, 34, 99, 58, 30, 82, 21, 80, 53, 31, 71, 57, 56, 38, 43, 94, 50, 78, 19, 66, 28, 61,22, 2, 46, 45, 32, 85, 83, 72, 23, 95, 90, 81, 68, 67, 1,70, 48, 87, 93, 40, 91, 29, 24, 17, 8, 3, 18, 15, 74, 69,64, 9, 26, 77, 51, 10, 79, 60, 88, 47, 5, 89, 20, 25, 35,7, 76, 12, 97, 52, 55, 33, 39, 86, 16, 37, 4, 62, 92]
    
    # last,t = Search(move,epo,a,ts,ss,iB)
    # s.save(ts,iB,last,t)
    # move = init()
    iB = False

    search = Search(move,epo,a,ts,ss,iB)    
    s.save(ts,iB,search.r_now_result,search.r_total)
    del search
        
    # iB = False
        
    # search1 = Search(move,epo,a,ts,ss,iB)    
    # s.save(ts,iB,search1.r_now_result,search1.r_total)
    # del search1


    s.write_data(isShow=True)