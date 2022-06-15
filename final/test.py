#加载红酒数据集
from sklearn.datasets import load_wine
#KNN分类算法
from sklearn.neighbors import KNeighborsClassifier
#分割训练集与测试集
from sklearn.model_selection import train_test_split
#导入numpy
import numpy as np
#加载数据集
wine_dataset=load_wine()
#查看数据集对应的键
# data 为数据集数据;target 为样本标签

#分割数据集，比例为 训练集：测试集 = 4:6
X_train,X_test,y_train,y_test=train_test_split(wine_dataset['data'],wine_dataset['target'],test_size=0.1,random_state=0)
#构建knn分类模型，并指定 k 值
KNN=KNeighborsClassifier(n_neighbors=3)
#使用训练集训练模型
KNN.fit(X_train,y_train)
#评估模型的得分
score=KNN.score(X_test,y_test)
print(score)

