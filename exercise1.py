"""
一个二维数组，左到右递增，上到下递增，输入这样一个二维数据和一个整数，判断整数是否在里面
《剑指offer》一书的80道题
"""
a=[
    [1,2,3],
    [4,5,6],
    [7,8,9]
]


def fun01(array_temp,number):
    if array_temp==[] or array_temp[0]==[]:
        return False
    last_arrary=array_temp[-1]
    if number<array_temp[0][0] or number>last_arrary[-1]:
        return False
    for i in array_temp:#i是一位数组
        if number not in i and number>i[-1]:
            continue
        for j in i:
            if j==number:
                return True
    return False

print(fun01(a,10))

