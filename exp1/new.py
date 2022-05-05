# -*- coding: utf-8 -*- 
# @Time : 2022/2/17 15:01 
# @Author : Orange
# @File : ts1.py.py
import copy, random, datetime
import matplotlib.pyplot as plt
import time
from dataloader import Dataloder

city_list = [[1, (1150.0, 1760.0)], [2, (630.0, 1660.0)], [3, (40.0, 2090.0)], [4, (750.0, 1100.0)],
             [5, (750.0, 2030.0)], [6, (1030.0, 2070.0)], [7, (1650.0, 650.0)], [8, (1490.0, 1630.0)],
             [9, (790.0, 2260.0)], [10, (710.0, 1310.0)], [11, (840.0, 550.0)], [12, (1170.0, 2300.0)],
             [13, (970.0, 1340.0)], [14, (510.0, 700.0)], [15, (750.0, 900.0)], [16, (1280.0, 1200.0)],
             [17, (230.0, 590.0)], [18, (460.0, 860.0)], [19, (1040.0, 950.0)], [20, (590.0, 1390.0)],
             [21, (830.0, 1770.0)], [22, (490.0, 500.0)], [23, (1840.0, 1240.0)], [24, (1260.0, 1500.0)],
             [25, (1280.0, 790.0)], [26, (490.0, 2130.0)], [27, (1460.0, 1420.0)], [28, (1260.0, 1910.0)],
             [29, (360.0, 1980.0)]
             ]


class Taboo_search:
    def __init__(self, city_list, candidate_count, taboo_list_length, iteration_count, is_random=True):

        self.city_list = city_list  # 城市列表
        self.candidate_count = candidate_count  # 候选集合长度
        self.taboo_list_length = taboo_list_length  # 禁忌长度
        self.iteration_count = iteration_count  # 迭代次数
        self.min_route, self.min_cost = self.random_first_full_road() if is_random else self.greedy_first_full_road()  # 最小解；最小目标值

        self.taboo_list = []  # 禁忌表

    # 计算两城市间的距离
    def city_distance(self, city1, city2):
        distance = ((float(city1[1][0] - city2[1][0])) ** 2 + (float(city1[1][1] - city2[1][1])) ** 2) ** 0.5
        return distance

    # 获取当前城市邻居城市中距离最短的一个
    def next_shotest_road(self, city1, other_cities):
        tmp_min = 999999
        tmp_next = None
        for i in range(0, len(other_cities)):
            distance = self.city_distance(city1, other_cities[i])
            # print(distance)
            if distance < tmp_min:
                tmp_min = distance
                tmp_next = other_cities[i]
        return tmp_next, tmp_min

    # 随机生成初始线路
    def random_first_full_road(self):
        cities = copy.deepcopy(self.city_list)
        cities.remove(cities[0])
        route = copy.deepcopy(cities)
        # random.shuffle(route)
        # route = [[6, (1030.0, 2070.0)], [5, (750.0, 2030.0)], [29, (360.0, 1980.0)], [3, (40.0, 2090.0)],
        #          [26, (490.0, 2130.0)], [9, (790.0, 2260.0)], [12, (1170.0, 2300.0)], [28, (1260.0, 1910.0)],
        #          [8, (1490.0, 1630.0)], [27, (1460.0, 1420.0)], [24, (1260.0, 1500.0)], [13, (970.0, 1340.0)],
        #          [16, (1280.0, 1200.0)], [23, (1840.0, 1240.0)], [7, (1650.0, 650.0)], [25, (1280.0, 790.0)],
        #          [19, (1040.0, 950.0)], [11, (840.0, 550.0)], [22, (490.0, 500.0)], [17, (230.0, 590.0)],
        #          [14, (510.0, 700.0)], [18, (460.0, 860.0)], [15, (750.0, 900.0)], [4, (750.0, 1100.0)],
        #          [10, (710.0, 1310.0)], [20, (590.0, 1390.0)], [2, (630.0, 1660.0)],
        #          [21, (830.0, 1770.0)]]  # 将初始值设置为遗传算法的最优值

        cost = self.route_cost(route)
        return route, cost

    # 根据贪婪算法获取初始线路
    def greedy_first_full_road(self):
        remain_city = copy.deepcopy(self.city_list)
        current_city = remain_city[0]
        road_list = []
        remain_city.remove(current_city)
        all_distance = 0
        while len(remain_city) > 0:
            next_city, distance = self.next_shotest_road(current_city, remain_city)
            all_distance += distance
            road_list.append(next_city)
            remain_city.remove(next_city)
            current_city = next_city
        all_distance += self.city_distance(self.city_list[0], road_list[-1])
        return road_list, round(all_distance, 2)

    # 随机交换2个城市位置
    def random_swap_2_city(self, route):
        # print(route)
        road_list = copy.deepcopy(route)
        two_rand_city = random.sample(road_list, 2)
        # print(two_rand_city)
        index_a = road_list.index(two_rand_city[0])
        index_b = road_list.index(two_rand_city[1])
        road_list[index_a] = two_rand_city[1]
        road_list[index_b] = two_rand_city[0]
        return road_list, sorted(two_rand_city)

    # 计算线路路径长度
    def route_cost(self, route):
        road_list = copy.deepcopy(route)
        current_city = self.city_list[0]
        while current_city in road_list:
            road_list.remove(current_city)
        all_distance = 0
        while len(road_list) > 0:
            distance = self.city_distance(current_city, road_list[0])
            all_distance += distance
            current_city = road_list[0]
            road_list.remove(current_city)
        all_distance += self.city_distance(current_city, self.city_list[0])
        return round(all_distance, 2)

    # 获取下一条线路
    def single_search(self, route):
        # 生成候选集合列表和其对应的移动列表
        candidate_list = []
        candidate_move_list = []
        while len(candidate_list) < self.candidate_count: # 在候选集合里放candidate_count条不重复路径
            tmp_route, tmp_move = self.random_swap_2_city(route)
            # print("tmp_route:",tmp_route)
            if tmp_route not in candidate_list:
                candidate_list.append(tmp_route)
                candidate_move_list.append(tmp_move)
        # 计算候选集合各路径的长度
        candidate_cost_list = []
        for candidate in candidate_list:
            candidate_cost_list.append(self.route_cost(candidate))
        # print(candidate_list)

        min_candidate_cost = min(candidate_cost_list)  # 候选集合中最短路径
        min_candidate_index = candidate_cost_list.index(min_candidate_cost)
        min_candidate = candidate_list[min_candidate_index]  # 候选集合中最短路径对应的线路
        move_city = candidate_move_list[min_candidate_index]

        if min_candidate_cost < self.min_cost:
            # 若满足这个条件不管禁忌对象是否在禁忌表内，都直接更新禁忌表
            self.min_cost = min_candidate_cost
            self.min_route = min_candidate
            if move_city in self.taboo_list:  # 破禁法则，当此移动导致的值更优，则无视该禁忌列表
                self.taboo_list.remove(move_city)
            if len(self.taboo_list) >= self.taboo_list_length:  # 判断该禁忌列表长度是否以达到限制，是的话移除最初始的move
                self.taboo_list.remove(self.taboo_list[0])
            self.taboo_list.append(move_city)  # 将该move加入到禁忌列表
            return min_candidate

        else:
            # 当未找到更优路径时，选择次优路线，如果该次优路线在禁忌表里，则更次一层，依次类推，找到一条次优路线
            if move_city in self.taboo_list:
                tmp_min_candidate = min_candidate
                tmp_move_city = move_city

                while move_city in self.taboo_list:  # 若候选最优禁忌对象已经在T表，寻找次优禁忌对象，若已在T表，.....
                    candidate_list.remove(min_candidate)
                    candidate_cost_list.remove(min_candidate_cost)
                    candidate_move_list.remove(move_city)

                    min_candidate_cost = min(candidate_cost_list)  # 候选集合中次优路径
                    min_candidate_index = candidate_cost_list.index(min_candidate_cost)
                    min_candidate = candidate_list[min_candidate_index]  # 候选集合中最短路径对应的线路
                    move_city = candidate_move_list[min_candidate_index]
                    if len(candidate_list) < 10:  # 防止陷入死循环，在候选集个数小于10的时候跳出
                        min_candidate = tmp_min_candidate
                        move_city = tmp_move_city
            if len(self.taboo_list) >= self.taboo_list_length:  # 判断该禁忌列表长度是否以达到限制，是的话移除最初始的move
                self.taboo_list.remove(self.taboo_list[0])
            self.taboo_list.append(move_city)
            return min_candidate

    # 进行taboo_search直到达到终止条件:循环100次
    def taboo_search(self):
        route = copy.deepcopy(self.min_route)
        for i in range(self.iteration_count):
            route = self.single_search(route)
            # if self.route_cost(route)<38000:
            #     break
        new_route = [self.city_list[0]]
        new_route.extend(self.min_route)
        new_route.append(self.city_list[0])  # 前后插入首个城市信息
        return new_route, self.min_cost


# 画线路图
def draw_line_pic(route, cost, duration, desc):
    x = []
    y = []
    for item in route:
        x.append(item[1][0])
        y.append(item[1][1])
    x_org = []
    y_org = []
    point_org = []
    for item in city_list:
        x_org.append(item[1][0])
        y_org.append(item[1][1])
        point_org.append(item[0])
    x0 = [x[0], ]
    y0 = [y[0], ]
    plt.plot(x, y)

    plt.scatter(x_org, y_org, marker="o", c='g')
    plt.scatter(x0, y0, marker="o", c="r")
    for i in range(len(city_list)):
        plt.text(x_org[i], y_org[i], point_org[i], ha='center', va='bottom', fontsize=10)
    plt.title("Taboo_Search(" + desc + ": " + str(cost) + ")")
    plt.show()


if __name__ == "__main__":
    ddd = Dataloder()
    city_list = []
    for i in range(0,100):
        tupl = (ddd.city_location[i][0],ddd.city_location[i][1]) 
        lis = [i+1,tupl]
        city_list.append(lis)
           
    dododo = []
    for i in range(44):
        print("============================")
        ts_random = Taboo_search(city_list=city_list, candidate_count=80, taboo_list_length=40, iteration_count=300)
    # ts_greedy = Taboo_search(city_list, candidate_count=80, taboo_list_length=100, iteration_count=1000,
                            #  is_random=False)
        start_time1 = datetime.datetime.now()
        route_random, cost_random = ts_random.taboo_search()
        end_time1 = datetime.datetime.now()
        duration1 = (end_time1 - start_time1).seconds
    # route_greedy, cost_greedy = ts_greedy.taboo_search()
        end_time2 = datetime.datetime.now()
        duration2 = (end_time2 - end_time1).seconds
    # draw_line_pic(route_random, cost_random, duration1, "random")
        print("最优路径：", route_random)
        dododo.append(cost_random)
        print("最短距离：", cost_random)
        print("随机TS耗时：",end_time1-start_time1)
        print(i)
        print("==============================")
    # draw_line_pic(route_greedy, cost_greedy, duration2, "greedy")

    print(dododo)