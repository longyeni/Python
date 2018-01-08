#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def calculate(startNumber, stopNumber):  # 大量使用除法系统处理速度过慢
    result = []
    while startNumber < stopNumber:
        if startNumber % 7 is 0:
            if startNumber % 5 != 0:
                result.append(startNumber)
        startNumber = startNumber + 1
    print(result)


def calculate2(startNumber, stopNumber):
    result = []
    if startNumber % 7 == 0 and startNumber % 5 != 0:
        pass
    else:
        startNumber = startNumber + 7 - startNumber % 7
    i = startNumber//7 % 5
    while startNumber < stopNumber:
        result.append(startNumber)
        i = i + 1
        if i == 5:
            startNumber = startNumber + 14
            i = 1
        else:
            startNumber = startNumber + 7
    print(result)


def calculate3(startNumber, stopNumber):  # 生成超长list占用空间过大
    result = list(filter(lambda x: x % 7 == 0 and x % 5 != 0, list(
        range(startNumber, stopNumber))))
    print(result)


startNumber = 2000
stopNumber = 3200
calculate3(startNumber, stopNumber)
calculate2(startNumber, stopNumber)
calculate(startNumber, stopNumber)
