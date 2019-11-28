import numpy as np

def encode(arr):
    count = 0
    rle_str = []
    prev = arr[0]
    if not arr: return []
    for i in range(len(arr)):
        if arr[i] != prev:
            rle_str.append((count, prev))
            count = 0
            prev = arr[i]
        count = count + 1
    else:
        rle_str.append((count, arr[i]))
        return rle_str

def decode(string):
    return ''.join([''.join([c] * n) for n, c in string])

def fill_2d_arr(arr, n, m):
    for i in range(n):
        mass = []
        for j in range(m):
            val = str(np.random.randint(4))
            mass.append(val)
        arr.append(mass)

def fill_1d_arr(arr, n, m):
    for i in range(m):
        for j in range(n):
            arr.append(arr2d[j][i])

def arr_to_sts(arr):
    string = ""
    for i in range(len(arr)):
        string += str(arr[i])
    return string

if __name__ == "__main__":
    print('Введите колическо строк')
    n = int(input())
    print('Введите колическо столбцов')
    m = int(input())
    # Двумерный массив
    arr2d = []
    # Одномерный масив
    arr1d = []
    fill_2d_arr(arr2d, n, m)
    fill_1d_arr(arr1d, n, m)
    print('Двумерный массив: ')
    print(arr2d)
    print('Преобразованный двумерный массив в одномерный массив:', arr1d)
    encode_rle = encode(arr1d)
    print('Преобразованная строка: ', encode_rle)
    print('Декодированая строка: ', decode(encode_rle))
    print('Количество элементов до сжатия: ', len(arr1d))
    print('Количество элементов после сжатия: ', len(encode_rle))
    print('Процент сжатия', int((len(encode_rle)/len(arr1d)) * 100))