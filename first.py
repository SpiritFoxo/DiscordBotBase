def GreatestNum(array):
    for i in range (0, len(array)-1):
        if array[0] >= array[1]:
            array.pop(1)
        else:
            array.pop(0)
    return array[0]

list = [1, 4, 3, 5, 7, 2]
print(GreatestNum(list))
