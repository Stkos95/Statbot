
import openpyxl

#Функция находит какое дейстивие было нажато в боте и выводит это действие, чтобы дальше увеличить значение на 1
def get_activity(value,data):
    return [i for i in data if value == i][0]



def operating_func(data, value):
    check_1time = data
    activity = get_activity(value=value, data=check_1time)
    data[activity] += 1








