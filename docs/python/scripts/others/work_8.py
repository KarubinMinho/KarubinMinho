import random


# 1.
class CreateNum:
    def __init__(self, range_min, range_max, nums_count=10):
        """
        :param range_min: int start of range(contain)
        :param range_max: int end of range(contain)
        :param nums_count: int total nums; default: 10
        """
        self.range_min = range_min
        self.range_max = range_max
        self.nums_count = nums_count

    def __repr__(self):
        return "<CreateNum range:{} nums: {}>".format(
            [self.range_min, self.range_max], self.nums_count)

    __str__ = __repr__

    def create_nums(self):
        """
        :return: list
        """
        num_range = list(range(self.range_min, self.range_max + 1))
        return random.choices(num_range, k=self.nums_count)


n = CreateNum(1, 5, 20)
print(n)
print(n.create_nums())
print('=' * 30)

# 2.
x = CreateNum(0, 10, 10)
y = x
coordinate = zip(x.create_nums(), y.create_nums())
for i in coordinate:
    print(i)
print('=' * 30)

# 3.


class CarManage:
    def __init__(self, mark, color, price, speed):
        self.mark = mark
        self.color = color
        self.price = price
        self.speed = speed

    def __repr__(self):
        return "<CarManage mark:{} color:{} price:{} speed:{}>".format(
            self.mark, self.color, self.price, self.speed)

    def add_car(self, all_info):
        info = dict(
            mark=self.mark,
            color=self.color,
            price=self.color,
            speed=self.speed)
        all_info['car_info'].append(info)

    @staticmethod
    def show_all_info(all_info):
        for key in all_info['car_info']:
            print(key)


base_info = {'car_info': []}
buick = CarManage('Buick', 'red', '150000', '130km/h')
buick02 = CarManage('Buick', 'white', '180000', '120km/h')
honda = CarManage('Honda', 'black', '250000', '140km/h')
buick.add_car(base_info)
buick02.add_car(base_info)
honda.add_car(base_info)
CarManage.show_all_info(base_info)  # or instance.show_all_info(base_info)
