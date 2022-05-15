import numpy as np
from search import Search
"""
模拟退火实验作业
人工智能1903班
王萱
20195235
"""

def main():
    search = Search(temp0=300,temp=400,r=0.98,deltaT=4,isDelta=True,inner_count=5)
    # search.search(temp0=300,temp=4000,r=0.98,deltaT=4,isDelta=True,inner_count=50)
    search.exp1()

    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()