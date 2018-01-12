#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlwt
import re


def fore_colour(forecolour, bold):  # 可随意设置颜色，
    # 颜色值参考 https://secure.simplistix.co.uk/svn/xlwt/trunk/xlwt/Style.py
    # https://www.crifan.com/python_xlwt_set_cell_background_color/
    style = xlwt.easyxf(
        'pattern: pattern solid, fore_colour %s; font: bold %s;' % (
            forecolour, bold))
    return style


def GetInfoFromLog(logFile):
    action = []
    actionTime = []
    with open(logFile, 'r', encoding='utf8') as logFile:
        lines = logFile.readlines(100000)  # 带缓存的文件读取，读取效率高
        if not lines:
            pass
        for line in lines:
            info = re.match(
                    r'^[0-9\:\s\/\,]{21}ACTION\s(\w{1,50})\s\[finished\][\w\:\s\=]{1,50}\=([0-9\.]{1,10})sec', line)
            if info:
                action.append(info.group(1))
                actionTime.append(info.group(2))
        return action, actionTime


def CalAvg(action, actionTime):
    actionList = set(action)
    result = [['runNum', 'actionName', 'timeAvg'], ]
    for actionName in actionList:
        i = 0
        timeAvg = 0
        runNum = 0
        for b in action:
            if b == actionName:
                runNum = runNum + 1
                timeAvg = timeAvg + float(actionTime[i])
            i = i + 1
        timeAvg = float('%.3f' % float(timeAvg/runNum))
        result.append([runNum, actionName, timeAvg])
    result = result[0:1] + sorted(result[1:len(result)])
    return result


def WriteExcel(sheetName, actionInfo, excelName):
    myexcel = xlwt.Workbook(encoding='ascii')
    mysheet = myexcel.add_sheet(sheetName)
    row = 0
    for item in actionInfo:
        column = 0
        while column < len(item):
            if row == 0:
                style = fore_colour('aqua', 'on')
                mysheet.write(row, column, item[column], style)
            elif isinstance(item[column], float) and item[column] > 2:
                style = fore_colour('yellow', 'off')
                mysheet.write(row, column, item[column], style)
            else:
                mysheet.write(row, column, item[column])
            column = column+1
        row = row+1
    myexcel.save(excelName)


if __name__ == '__main__':
    sheetName = 'CalAvgTime'
    logFile = '.\Practice\CalAvgTime.txt'
    excelName = '.\Practice\CalAvgTime.xls'
    action, actionTime = GetInfoFromLog(logFile)
    actionInfo = CalAvg(action, actionTime)
    WriteExcel(sheetName, actionInfo, excelName)
