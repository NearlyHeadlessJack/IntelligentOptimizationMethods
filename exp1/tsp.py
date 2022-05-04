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
from lists import TList, PList,Cache
import random,math


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

def search(mov,epochs,alpha,tlist,isBan=False):
    
    optimum_dis = cal(mov)
    total_mov = 0
    
    for epoch in range(1,epochs):
        last_mov = mov
        now_result = cal(mov)
        result = cal(mov)
        i = 0
        cache = Cache()
        total_mov += 1
        while result>=now_result:
            mov = last_mov
            i +=1
            
            # print("in epoch" + str(epoch))
            
            a,b = randmov()
            plist.add({a,b})
            c = mov[b-1]
            mov[b-1] = mov[a-1]
            mov[a-1] = c
            result = cal(mov) + alpha*plist.map[1][plist.iter({a,b},isBan)]
            cache.add(a,b,result)
            # print("result:" + str(result))
            if i>800:
                mov = last_mov
                result,a,b=cache.minimum()
                c = mov[b-1]
                mov[b-1] = mov[a-1]
                mov[a-1] = c
                break
            if tlist.search({a,b}):
                if result<optimum_dis:
                    optimum_dis = cal(mov)
                    tlist.iter({a,b})
                else:
                    
                    
            
            
        if not tlist.search({a,b}):
            print(tlist.list)
            tlist.iter({a,b})
            if result<optimum_dis:
                # print("change")
                optimum_dis = cal(mov)
        else:
            print("exist")
            if result<optimum_dis:
                
                optimum_dis = cal(mov)
                tlist.iter({a,b})
            else:
                mov = last_mov
    best_mov = mov
    best_result = cal(best_mov)
        
    return best_result,total_mov
                
    
    
def exp1():
    exp_result = []
    exp_tsize = []
    exp_isBan = []
    exp_optimum = []
    exp_total = []
    for i in range(3,60):
        tlist.change_size(i)
        exp_tsize.append(i)
        exp_tsize.append(i)
        result,total = search(move,10,0.001,False)
        exp_isBan.append(0)
        exp_optimum.append(result)
        exp_total.append(total)
        tlist.change_size(i)
        result,total = search(move,10,0.001,True)
        exp_isBan.append(1)
        exp_optimum.append(result)
        exp_total.append(total)
        plist = PList()
    exp_result.append(exp_tsize)
    exp_result.append(exp_isBan)
    exp_result.append(exp_optimum)
    exp_result.append(exp_total)
    
    print(exp_result)
    with open(file = 'exp1.txt',mode = 'w+')as f:
        for exp in exp_result[0]:
            f.writelines(str(exp)+'\n')
        
    with open(file = 'exp2.txt',mode = 'w+')as f:
        for exp in exp_result[1]:
            f.writelines(str(exp)+'\n')
    with open(file = 'exp3.txt',mode = 'w+')as f:
        for exp in exp_result[2]:
            f.writelines(str(exp)+'\n')
    with open(file = 'exp4.txt',mode = 'w+')as f:
        for exp in exp_result[3]:
            f.writelines(str(exp)+'\n')
    
    
    
def exp2():
    exp_result = []
    exp_tsize = []
    exp_isBan = []
    exp_optimum = []
    exp_total = []
    
    for i in range(1,100):
        tlist = TList(60)
        plist = PList()
        move = init()
        exp_tsize.append(60)
        exp_tsize.append(60)
        result,total = search(move,10,0.001,False)
        exp_isBan.append(0)
        exp_optimum.append(result)
        exp_total.append(total)
        tlist = TList(60)
        plist = PList()
        result,total = search(move,10,0.001,True)
        exp_isBan.append(1)
        exp_optimum.append(result)
        exp_total.append(total)
        
    exp_result.append(exp_tsize)
    exp_result.append(exp_isBan)
    exp_result.append(exp_optimum)
    exp_result.append(exp_total)
    
    print(exp_result)
    with open(file = 'exp1.txt',mode = 'w+')as f:
        for exp in exp_result[0]:
            f.writelines(str(exp)+'\n')
        
    with open(file = 'exp2.txt',mode = 'w+')as f:
        for exp in exp_result[1]:
            f.writelines(str(exp)+'\n')
    with open(file = 'exp3.txt',mode = 'w+')as f:
        for exp in exp_result[2]:
            f.writelines(str(exp)+'\n')
    with open(file = 'exp4.txt',mode = 'w+')as f:
        for exp in exp_result[3]:
            f.writelines(str(exp)+'\n')
    
if __name__ == "__main__":
    
    
    d = Dataloder()
    # tlist = TList(20)
    plist = PList()
    move = init()
    move =[49, 65, 63, 41, 13, 96, 6, 11, 59, 27, 14, 100, 44, 42, 54, 98, 73, 84, 75, 36, 34, 99, 58, 30, 82, 21, 80, 53, 31, 71, 57, 56, 38, 43, 94, 50, 78, 19, 66, 28, 61, 22, 2, 46, 45, 32, 85, 83, 72, 23, 95, 90, 81, 68, 67, 1, 70, 48, 87, 93, 40, 91, 29, 24, 17, 8, 3, 18, 15, 74, 69, 64, 9, 26, 77, 51, 10, 79, 60, 88, 47, 5, 89, 20, 25, 35, 7, 76, 12, 97, 52, 55, 33, 39, 86, 16, 37, 4, 62, 92]
    print(move)
    exp_result = []
    exp_tsize = []
    exp_isBan = []
    exp_optimum = []
    exp_total = []
    for i in range(1,11):
        move =[49, 65, 63, 41, 13, 96, 6, 11, 59, 27, 14, 100, 44, 42, 54, 98, 73, 84, 75, 36, 34, 99, 58, 30, 82, 21, 80, 53, 31, 71, 57, 56, 38, 43, 94, 50, 78, 19, 66, 28, 61, 22, 2, 46, 45, 32, 85, 83, 72, 23, 95, 90, 81, 68, 67, 1, 70, 48, 87, 93, 40, 91, 29, 24, 17, 8, 3, 18, 15, 74, 69, 64, 9, 26, 77, 51, 10, 79, 60, 88, 47, 5, 89, 20, 25, 35, 7, 76, 12, 97, 52, 55, 33, 39, 86, 16, 37, 4, 62, 92]
        optimum_dis = 1.0
        tlist3 = TList(4000)
        plist = PList()
        exp_tsize.append(4000)
        result,total = search(move,100,0.001,tlist3,True)
        exp_isBan.append(1)
        exp_optimum.append(result)
        exp_total.append(total)
        

        
    
    exp_result.append(exp_tsize)
    exp_result.append(exp_isBan)
    exp_result.append(exp_optimum)
    exp_result.append(exp_total)
    
    print(exp_result)
    with open(file = 'exp1.txt',mode = 'w+')as f:
        for exp in exp_result[0]:
            f.writelines(str(exp)+'\n')
        
    with open(file = 'exp2.txt',mode = 'w+')as f:
        for exp in exp_result[1]:
            f.writelines(str(exp)+'\n')
    with open(file = 'exp3.txt',mode = 'w+')as f:
        for exp in exp_result[2]:
            f.writelines(str(exp)+'\n')
    with open(file = 'exp4.txt',mode = 'w+')as f:
        for exp in exp_result[3]:
            f.writelines(str(exp)+'\n')
    
    
    
    

    
    
    