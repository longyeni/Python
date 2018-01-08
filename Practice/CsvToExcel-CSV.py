#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import xlwt


def CsvToExcel(sheetName, csvFile, excelName):
    myexcel = xlwt.Workbook(encoding='ascii')  # 新建excel文件
    mysheet = myexcel.add_sheet(sheetName, cell_overwrite_ok='True')
    # 新建sheet页，允许复写单元格
    csvFile = open(csvFile, 'r', encoding='utf8')  # open()编码格式需明确指定
    reader = list(csv.reader(csvFile))  # 每一行读成一个list
    reader = reader[0:1] + sorted(reader[1:len(reader)])
    row = 0
    for item in reader:
        column = 0
        while column < len(item):
            mysheet.write(row, column, item[column])
            if row == 0:
                style = fore_colour('aqua', 'on')
                mysheet.write(row, column, item[column], style)
            elif item[column] == '无货':
                style = fore_colour('yellow', 'off')
                mysheet.write(row, 1, item[1], style)
            elif len(item) < 4 or item[3] == '':
                style = fore_colour('red', 'off')
                mysheet.write(row, 1, item[1], style)
            column = column+1
        row = row+1
    myexcel.save(excelName)


def fore_colour(forecolour, bold):  # 可随意设置颜色，
    # 颜色值参考 https://secure.simplistix.co.uk/svn/xlwt/trunk/xlwt/Style.py
    # https://www.crifan.com/python_xlwt_set_cell_background_color/
    style = xlwt.easyxf(
        'pattern: pattern solid, fore_colour %s; font: bold %s;' % (
            forecolour, bold))
    return style


if __name__ == '__main__':
    sheetName = '库存状态'
    csvFile = 'CsvToExcel.csv'
    excelName = 'CsvToExcel.xls'
    CsvToExcel(sheetName, csvFile, excelName)
