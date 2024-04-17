from MyString import *


class MyExcept(Exception):
    def __init__(self, s):
        self.str_error = s


class KPV:
    def __init__(self):
        self.__arr_val = []
        self.__size = 0
        self.__str_goods = [goodsA1, goodsB1, goodsA2, goodsB2]
        self.is_recording = 0

    def add_arr(self, n: float):
        self.__arr_val.append(n)
        self.__size += 1
        if self.__size > 3:
            self.is_recording = 0

    def get_str(self):
        return f"Введите {self.__str_goods[self.__size]}"

    def reset_data(self):
        self.__arr_val.clear()
        self.__size = 0
        self.is_recording = 0

    def get_data(self):
        local_a1 = self.__arr_val[0]
        local_b1 = self.__arr_val[1]
        local_a2 = self.__arr_val[2]
        local_b2 = self.__arr_val[3]
        return local_a1, local_b1, local_a2, local_b2


class MarketEquilibrium:
    def __init__(self):
        self.__arr_val = []
        self.__size = 0
        self.__arr_str = [a, b, c, d]  # из файла MyString
        self.__info_str = info
        self.is_recording = 0

    def add_arr(self, n: float):
        self.__arr_val.append(n)
        self.__size += 1
        if self.__size > 3:
            self.is_recording = 0

    def get_str(self):
        return f"Введите коэффициент {self.__arr_str[self.__size]}"

    def reset_data(self):
        self.__arr_val.clear()
        self.__size = 0
        self.is_recording = 0

    def get_data(self):
        local_a = self.__arr_val[0]
        local_b = self.__arr_val[1]
        local_c = self.__arr_val[2]
        local_d = self.__arr_val[3]

        return local_a, local_b, local_c, local_d

    def get_info(self):
        return self.__info_str


class DeficitAndSurplus:
    def __init__(self):
        self.__arr_val = []
        self.__size = 0
        self.__arr_str = [a1, b1, c1, d1, e1]
        self.__info = info
        self.is_recording = 0

    def add_arr(self, n: float):
        self.__arr_val.append(n)
        self.__size += 1
        if self.__size > 4:
            self.is_recording = 0

    def get_str(self):
        return f"Введите коэффициент {self.__arr_str[self.__size]}"

    def get_numb_arr(self, n):
        return self.__arr_val[n]

    def get_info(self):
        return self.__info

    def reset_data(self):
        self.__arr_val.clear()
        self.__size = 0
        self.is_recording = 0


class ProfitCompany:
    def __init__(self):
        self.__arr_numb = []
        self.__size_numb = 0
        self.__getting_data_for_arr_numb = True

        self.__all_costs = [[], []]
        self.__size_costs = 0
        self.__getting_data_for_costs = True
        self.__getting_data_for_first_costs = True

        self.__arr_str = [str1, str2, str3, str4]
        self.__current_quest = 0

        self.is_recording = 1

    def add_numb(self, n: int):
        self.__arr_numb.append(n)
        self.__size_numb += 1

        self.__current_quest += 1

        if self.__size_numb >= 2:
            self.__getting_data_for_arr_numb = False

    def add_costs(self, n: int):  # list or int
        if self.__getting_data_for_first_costs:
            self.__all_costs[0].append(n)
        else:
            self.__all_costs[1].append(n)
        self.__size_costs += 1

        # При заполнении массива all_costs[0] (постоянные издержки),
        if self.__size_costs >= 5:
            self.__current_quest += 1

            if self.__getting_data_for_costs == 0:
                self.is_recording = False
            else:
                self.__getting_data_for_costs = False
                self.__getting_data_for_first_costs = False
                self.__size_costs = 0

    def count_costs(self):
        return self.__size_costs

    def go_to_button_has_worked(self):
        return not self.__getting_data_for_costs

    def in_progress_first_part(self):
        return self.__getting_data_for_arr_numb

    def get_str(self):
        s = self.__arr_str[self.__current_quest]
        return s

    def getting_data(self):
        return self.__getting_data_for_costs

    def abort_getting_data_for_first_arr(self):
        self.__current_quest += 1
        self.__getting_data_for_costs = False
        self.__getting_data_for_first_costs = False
        self.__size_costs = 0

    def result(self):
        q = self.__arr_numb[0]
        p = self.__arr_numb[1]
        total_const_costs = 0
        total_change_costs = 0
        const_costs = self.__all_costs[0]
        change_costs = self.__all_costs[1]

        for i in range(len(const_costs)):
            total_const_costs += const_costs[i][1]
        for i in range(len(change_costs)):
            total_change_costs += change_costs[i][1]

        profit = q * (p - total_change_costs) - total_const_costs

        return self.create_res(profit, total_const_costs, total_change_costs)

    def create_res(self, profit, t1, t2):
        s1 = ''
        change = self.__all_costs[1]
        for i in range(len(change)):
            s1 = s1 + ' ' + change[i][0] + ' ' + str(change[i][1]) + ','

        s2 = ''
        const = self.__all_costs[0]
        for i in range(len(const)):
            s2 = s2 + ' ' + const[i][0] + ' ' + str(const[i][1]) + ','
        s3 = (f'При реализации {self.__arr_numb[0]} единиц продукции по {self.__arr_numb[1]} '
              f'руб за единицу товара и уровне переменных издержек в {t2} руб./ единицу товара '
              f'(включая:{s1}) и постоянных издержках в {t1}руб./единицу товара (включая: '
              f'{s2}) прибыль составить {profit}.')
        return s3

    def reset_data(self):
        self.__arr_numb.clear()
        self.__size_numb = 0
        self.__getting_data_for_arr_numb = True

        self.__all_costs.clear()
        self.__all_costs = [[], []]
        self.__size_costs = 0
        self.__getting_data_for_costs = True
        self.__getting_data_for_first_costs = True

        self.__arr_str = [str1, str2, str3, str4]
        self.__current_quest = 0

        self.is_recording = True
