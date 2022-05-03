'''
TSP Benchmark问题求解
使用数据KroA100
初始解随机产生
领域移动方式为2-opt
采用基于概率的邻域搜索方式
惩罚因子设为0.001
采用t-检验的方式分析算法性能
'''
import dataloader as d
from lists import TList, PList

if __name__ == "__main__":
    
    d.load()
    tlist = TList(4)
    plist = PList()
    

    
    
    