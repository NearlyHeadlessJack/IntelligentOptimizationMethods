from savedata import SaveData
from lists import *
from dataloader import *
import numpy as np
from numpy import random
from numpy import sqrt


class Search:

    def __init__(self, save_data, init_cities, alpha=0.001 * 40000, subset_size=80, epochs=200, tabu_size=5,
                 is_show=True, is_ban_plist=False):
        self.saveData = save_data
        self.tabu_list = TList(tabu_size)
        self.p_list = PList()
        dataloader = Dataloder()
        self.original_city = dataloader.cities
        self.city_copy = dataloader.cities
        self.epochs = epochs
        self.subset_size = subset_size
        self.alpha = alpha
        self.optimum = 50000
        self.now_distance = 50000

    def random_mov(self, route_now):
        exchange_cities = random.choice(route_now[0], 2) - 1
        ex = exchange_cities

        route_now[1][ex[0]], route_now[1][ex[1]] = route_now[1][ex[1]], route_now[1][ex[0]]

        route_now[0][ex[0]], route_now[0][ex[1]] = route_now[0][ex[1]], route_now[0][ex[0]]

        return route_now, int(route_now[0][ex[0]]), int(route_now[0][ex[1]])

    def distance_calculation(self, route_now):

        r = route_now
        distance = 1.0
        for i in range(1, 100):
            distance += sqrt(((r[1][i][0] - r[1][i - 1][0]) ** 2) + ((r[1][i][1] - r[1][i - 1][1]) ** 2))
        distance += sqrt(((r[1][99][0] - r[1][0][0]) ** 2) + ((r[1][99][1] - r[1][0][1]) ** 2))

        return distance

    def search_once(self, route_now):
        subset_size = self.subset_size
        route = route_now

        random_subsets = []
        subsets_distance = []
        random_movsets = []

        for i in range(subset_size):
            route_, mov1, mov2 = self.random_mov(route)
            random_movsets.append({mov1, mov2})
            random_subsets.append(route_)
            subsets_distance.append(
                self.distance_calculation(route_) + self.alpha * self.p_list.iter({mov1, mov2}))

        random_subsets = np.array(random_subsets)
        subsets_distance = np.array(subsets_distance)

        index_of_order = np.argsort(subsets_distance)

        for j in range(subset_size):
            ordered_index = index_of_order[j]
            _set = random_movsets[ordered_index]
            _distance = subsets_distance[ordered_index]
            _subset = random_subsets[ordered_index]

            if not self.tabu_list.search(_set):
                self.tabu_list.iter(_set)
                self.now_distance = _distance

                if self.now_distance < self.optimum:
                    self.optimum = self.now_distance
                return _subset

            else:
                if _distance < self.optimum:
                    self.tabu_list.iter(_set)
                    self.now_distance = _distance
                    self.optimum = self.now_distance
                    return _subset
                else:
                    continue
        return route_now

    def search(self):
        epochs = self.epochs
        route = self.original_city
        for i in range(epochs):
            route = self.search_once(route)

        print("best:")
        print(self.optimum)
        print("latest:")
        print(self.now_distance)
