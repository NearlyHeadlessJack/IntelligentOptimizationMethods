import numpy as np  # 导入NumPy函数库
import math

POP_NUM = 200  # 种群大小200
Chromosome_size = 100  # 基因的位数个数100位
ITER_NUM = 500  # 迭代500次
CROSS_RATE = 0.66  # 交叉率(Cross rate)取值范围一般为0.4～0.99
MUT_RATE = 0.00066  # 变异率(Mutation rate)取值范围一般为0.0001～0.1
Fit_value = []  # 适应值
NewChrom_new = []  # 后代

# deceptive function DF2的四位二进制
A = [0, 0, 0, 0]
B = [0, 0, 0, 1]
C = [0, 0, 1, 0]
D = [0, 0, 1, 1]
E = [0, 1, 0, 0]
F = [0, 1, 0, 1]
G = [0, 1, 1, 0]
H = [0, 1, 1, 1]
I = [1, 0, 0, 0]
J = [1, 0, 0, 1]
K = [1, 0, 1, 0]
L = [1, 0, 1, 1]
M = [1, 1, 0, 0]
N = [1, 1, 0, 1]
O = [1, 1, 1, 0]
P = [1, 1, 1, 1]

Group = np.random.randint(2, size=(POP_NUM, Chromosome_size))  # 产生初始种群  


def binToDec(Group):
    """
    计算初始欺骗函数值=计算适值
    """
    for m in range(POP_NUM):
        sum = 0
        for n in range(25):
            x_bits = list(Group[m][4 * n:4 * (n + 1)])

            if (x_bits == A):
                sum = sum + 4
            elif (x_bits == B):
                sum = sum + 1
            elif (x_bits == C):
                sum = sum + 1
            elif (x_bits == D):
                sum = sum + 2
            elif (x_bits == E):
                sum = sum + 1
            elif (x_bits == F):
                sum = sum + 2
            elif (x_bits == G):
                sum = sum + 2
            elif (x_bits == H):
                sum = sum + 3
            elif (x_bits == I):
                sum = sum + 1
            elif (x_bits == J):
                sum = sum + 2
            elif (x_bits == K):
                sum = sum + 2
            elif (x_bits == L):
                sum = sum + 3
            elif (x_bits == M):
                sum = sum + 2
            elif (x_bits == N):
                sum = sum + 3
            elif x_bits == O:
                sum = sum + 3
            elif x_bits == P:
                sum = sum + 0

        Fit_value.append(sum)

    return Fit_value  # 返回适应值


# GA选择操作
def Choose(Group, fitness):  # 遗传操作-轮盘赌选择法

    Target = np.random.choice(np.arange(POP_NUM), size=POP_NUM, replace=True,
                              p=fitness / fitness.sum())  # 计算选择概率
    return Group[Target]


# GA交叉操作
def Crossover(LastChrom, Entity):
    if np.random.rand() < CROSS_RATE:

        m = np.random.randint(0, POP_NUM, size=1)
        Cross_Cut1 = int(np.random.randint(0, Chromosome_size, size=1))  # 选择交叉切点
        Cross_Cut2 = int(np.random.randint(0, Chromosome_size, size=1))
        if (Cross_Cut1 < Cross_Cut2):
            LastChrom[Cross_Cut2 - Cross_Cut1:Chromosome_size - Cross_Cut1] = Entity[m, Cross_Cut2:]
        else:
            LastChrom[Cross_Cut1 - Cross_Cut2:Chromosome_size - Cross_Cut2] = Entity[m, Cross_Cut1:]

    return LastChrom


# GA变异操作
def variation(NewChrom):
    for point in range(Chromosome_size):
        if np.random.rand() < MUT_RATE:
            NewChrom[point] = 1 if NewChrom[point] == 0 else 0
    return NewChrom  # 返回新子代


def NewChrom_value(Group):  # 新产生Chromosome的函数值
    sum = 0  # 初始化函数值为0

    for n in range(25):

        y_bits = list(Group[4 * n:4 * (n + 1)])

        if (y_bits == A):
            sum = sum + 4
        elif (y_bits == B):
            sum = sum + 1
        elif (y_bits == C):
            sum = sum + 1
        elif (y_bits == D):
            sum = sum + 2
        elif (y_bits == E):
            sum = sum + 1
        elif (y_bits == F):
            sum = sum + 2
        elif (y_bits == G):
            sum = sum + 2
        elif (y_bits == H):
            sum = sum + 3
        elif (y_bits == I):
            sum = sum + 1
        elif (y_bits == J):
            sum = sum + 2
        elif (y_bits == K):
            sum = sum + 2
        elif (y_bits == L):
            sum = sum + 3
        elif (y_bits == M):
            sum = sum + 2
        elif (y_bits == N):
            sum = sum + 3
        elif (y_bits == O):
            sum = sum + 3
        elif (y_bits == P):
            sum = sum + 0

    return sum  # 返回函数值


for n in range(ITER_NUM):  # 迭代计算
    F_values = binToDec(Group)  # 计算适应值对应的值

    Group = Choose(Group, np.array(F_values))
    pop_copy = Group.copy()

    for LastChrom in Group:
        NewChrom = Crossover(LastChrom, Group)
        NewChrom = variation(NewChrom)

        Gene = NewChrom_value(NewChrom)
        if (Gene > np.median(F_values)):  # 子代适应值超过中位数则接受
            pop_copy[np.argmin(F_values), :] = NewChrom  # 将原种群中的适应值最小的一个替换掉
            F_values[np.argmin(F_values)] = Gene  # 更新适应值

    Group = pop_copy.copy()

    Fit_value.clear()  # 适应值清零
    values_new = binToDec(pop_copy)
    x = np.argmax(values_new)
    print("Best Chromosome: ""\n", Group[x])  # 打印最大值对应的基因
    print("Maximal Function Value: ", values_new[x])  # 打印最大函数值

    Fit_value.clear()  # 适应值清零
