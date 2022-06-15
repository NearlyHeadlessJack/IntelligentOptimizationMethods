# -*- encoding: utf-8 -*-
 
import random
import math
import numpy as np
import pandas as pd
from Genetic_algorithm import GA
import matplotlib.pyplot as plt
#import lightgbm as lgb
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
 
class FeatureSelection(object):
    def __init__(self, aLifeCount=10):
        self.columns = ['target', 'fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides',
                        'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol']

        self.wine = pd.read_csv("wine_3cls 2.csv", low_memory=False, usecols=self.columns)
 
       # self.Xtrain, self.Xtest, self.Ytrain, self.Ytest = train_test_split(self.wine , self.wine.target, test_size=0.1)
 
        self.lifeCount = aLifeCount
        self.ga = GA(aCrossRate=0.6,
                     aMutationRage=0.1,
                     aLifeCount=self.lifeCount,
                     aGeneLenght=len(self.columns) - 1,
                     aMatchFun=self.matchFun())
 
    def knn_score(self, order):
 
        #print("order:  " ,order)
        features = self.columns[1:]
        features_name = []
        features_name.append(self.columns[0])
        #print("features:  ", features)
        for index in range(len(order)):
            if order[index] == 1:
                features_name.append(features[index])
        #特征名
        #print("features_name:  " ,features_name)
        params = {
            'boosting': 'gbdt',
            'objective': 'binary',
            'metric': 'auc',
            'train_metric': False,
            'subsample': 0.8,
            'learning_rate': 0.8,
            'num_leaves': 96,
            'num_threads': 4,
            'max_depth': 5,
            'colsample_bytree': 0.8,
            'lambda_l2': 0.01,
            'verbose': -1,  # inhibit print info #
        }
        rounds = 100
 
        self.Xtrain, self.Xtest, self.Ytrain, self.Ytest = train_test_split(self.wine[features_name],self.wine[features_name].target, test_size=0.4)
        #print("self.wine[features_name]:  ", self.wine[features_name])
        #标准化
        transfer = StandardScaler()
        self.Xtrain = transfer.fit_transform(self.Xtrain)
        #print("self.Xtrain  ", self.Xtrain)
        self.Xtest = transfer.transform(self.Xtest)
        estimator = KNeighborsClassifier()
        # 加入网格搜索与交叉验证
         #参数准备
        param_dict = {"n_neighbors": [1, 3, 5, 7, 9]}
        estimator = GridSearchCV(estimator, param_grid=param_dict, cv=5)
        estimator.fit(self.Xtrain, self.Ytrain)
 
        # 方法2：计算准确率
        score = estimator.score(self.Xtest,self.Ytest)
        print("score：\n",score)
        # 最佳参数：best_params_
        print("最佳参数：\n", estimator.best_params_)
        # 最佳结果：best_score_
        print("最佳结果：\n", estimator.best_score_)
        # 最佳估计器：best_estimator_
        print("最佳估计器:\n", estimator.best_estimator_)
        # 交叉验证结果：cv_results_
        #print("交叉验证结果:\n", estimator.cv_results_)
        return score
 
    def matchFun(self):
        return lambda life: self.knn_score(life.gene)
    def run(self, n=0):
        distance_list = []
        generate = [index for index in range(1, n + 1)]
        while n > 0:
            self.ga.next()
            # distance = self.auc_score(self.ga.best.gene)
            distance = self.ga.score                      ####
            distance_list.append(distance)
            print(("第%d代 : 当前最好特征组合的线下验证结果为：%f") % (self.ga.generation, distance))
            n -= 1
 
        print('当前最好特征组合:')
        string = []
        flag = 0
        features = self.columns[1:]
        for index in self.ga.gene:                                  ####
            if index == 1:
                string.append(features[flag])
            flag += 1
        print(string)
        print('最高knn_score：', self.ga.score)                      ####
 
        '''画图函数'''
        plt.plot(generate, distance_list)
        plt.xlabel('generation')
        plt.ylabel('knn-score')
        plt.title('generation--knn-score')
        plt.grid()
        plt.show()
 
 
def main():
    fs = FeatureSelection(aLifeCount=5)
    rounds = 10    # 算法迭代次数 #
    fs.run(rounds)
 
 
if __name__ == '__main__':
    main()