import numpy as np
import pandas as pd
from random import randint

class Grid:
    def __init__(self):
        self.grid_vector = np.ones([10, 10])
        # start point
        self.grid_vector[0, 0] = 0
        self.sum_steps = np.zeros([10, 10])
        self.not_deliver_point = []
        self.path_list = [[[] for j in range(10)] for i in range(10)]

    def set_obstacle(self, location):
        for i in range(0, len(location)):
            self.grid_vector[location[i][0], location[i][1]] = np.nan
        self.obstacle_location = location
        # print(self.grid_vector)

    def avoid_obstacle(self, i, j):
        selection_list = []
        loc_list = []
        # Six directions
        if not pd.isna(self.sum_steps[i - 1, j]):
            selection_list.append(self.sum_steps[i - 1, j])
            loc_list.append([i - 1, j])
        if not pd.isna(self.sum_steps[i, j - 1]):
            selection_list.append(self.sum_steps[i, j - 1])
            loc_list.append([i, j - 1])
        if not pd.isna(self.sum_steps[i - 1, j - 1]):
            selection_list.append(self.sum_steps[i - 1, j - 1])
            loc_list.append([i - 1, j - 1])
        ''''
        if i + 1 < 10:
            if not pd.isna(self.sum_steps[i + 1, j]):
                selection_list.append(self.sum_steps[i + 1, j])
                loc_list.append([i + 1, j])
        if j + 1 < 10:
            if not pd.isna(self.sum_steps[i, j + 1]):
                selection_list.append(self.sum_steps[i, j + 1])
                loc_list.append([i, j + 1])
        if i + 1 < 10 and j + 1 < 10:
            if not pd.isna(self.sum_steps[i + 1, j + 1]):
                selection_list.append(self.sum_steps[i + 1, j + 1])
                loc_list.append([i + 1, j + 1])
        '''''
        if selection_list == []:
            loc = []
        else:
            loc = loc_list[selection_list.index(min(selection_list))]
        return loc

    def path_steps(self):
        self.sum_steps[0, 0] = self.grid_vector[0, 0]
        self.path_list[0][0].append([0, 0])
        for j in range(1, 10):
            if not pd.isna(self.grid_vector[0, j]):
                self.sum_steps[0, j] = self.sum_steps[0, j-1] + self.grid_vector[0, j]
                self.path_list[0][j] = self.path_list[0][j-1] + [[0, j]]
            else:
                self.sum_steps[0, j] = np.nan
            if not pd.isna(self.grid_vector[j, 0]):
                self.sum_steps[j, 0] = self.sum_steps[j - 1, 0] + self.grid_vector[j, 0]
                self.path_list[j][0] = self.path_list[j - 1][0] + [[j, 0]]
            else:
                self.sum_steps[j, 0] = np.nan

        for i in range(1, 10):
            for j in range(1, 10):
                # obstacle point
                if pd.isna(self.grid_vector[i, j]):
                    self.sum_steps[i, j] = np.nan
                min_loc = self.avoid_obstacle(i, j)
                if min_loc == []:
                    self.sum_steps[i, j] = np.nan
                    self.not_deliver_point.append([i, j])
                else:
                    self.path_list[i][j] = self.path_list[min_loc[0]][min_loc[1]] + [[i, j]]
                    self.sum_steps[i, j] = self.grid_vector[i, j] + self.sum_steps[min_loc[0], min_loc[1]]

        # delivered
        if not pd.isna(self.sum_steps[9][9]):
            # print(self.sum_steps)
            print(f"The number of steps is " + str(self.sum_steps[9][9]))
            print("The path is "+ str(self.path_list[9][9]))
            return True
        # Not delivered
        else:
            print("Unable to reach delivery point.")
            return False

    def remove_obstacle(self):
        flag = self.path_steps()
        remove_list = []
        for index in range(0, len(self.not_deliver_point)):
            loc = self.not_deliver_point[index]
            if flag:
                break
            while not flag:
                loc_list = [[loc[0] - 1, loc[1] - 1], [loc[0], loc[1] - 1], [loc[0] - 1, loc[1]]]
                for item in loc_list:
                    if item in self.obstacle_location:
                        self.obstacle_location.remove(item)
                        remove_list.append(item)
                        break
                    else:
                        continue
                self.__init__()
                grid.set_obstacle(self.obstacle_location)
                flag = self.path_steps()
                loc = self.not_deliver_point[len(self.not_deliver_point) - index - 1]
        if remove_list != []:
            print(f"The obstacles which need to be removed are" + str(remove_list))

if __name__ == '__main__':
    grid = Grid()
    start = [0, 0]
    end = [9, 9]
    # Phase 1
    print("---------This is Phase 1-----------")
    location_1 = [[9, 7], [8, 7], [6, 7], [6, 8]]
    grid.set_obstacle(location_1)
    grid.path_steps()
    # Phase 2
    print("---------This is Phase 2-----------")
    grid.__init__()
    location_2 = []
    check_list = location_2 + [start] + [end]
    while len(location_2) < 20:
        temp = [randint(0, 9), randint(0, 9)]
        if temp not in check_list:
            location_2.append(temp)
            check_list.append(temp)
    print(f"The obstacles' location is " + str(location_2))
    grid.set_obstacle(location_2)
    grid.remove_obstacle()
    ''''
    location_no = [[1, 1], [1, 0], [0, 1], [2, 2], [2, 0], [2, 1], [0, 2], [7, 6],
                   [6, 1], [4, 5], [3, 3], [0, 3], [5, 7], [2, 4], [9, 5], [1, 3], [7, 2], [9, 8], [8, 8], [8, 9]]
    grid.set_obstacle(location_no)
    '''''

