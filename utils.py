#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import datetime
import xlrd
import xlwt
from xlutils.copy import copy as xlcopy

help_text = "Выбери один из интересующих тебя разделов:"

start_text = "Привет!\n"

free_time = "Выбери дату:\n"

code_word = "1234"

alphabet = "авекмнорстухАВЕКМНОРСТУХ"

col_FIO = 1
row_DAY = 2


class simpleTime:
    def __init__(self, delta):
        d = datetime.datetime.now().day
        m = datetime.datetime.now().month
        y = datetime.datetime.now().year
        self.date = datetime.datetime(y,m,d)
        self.date += datetime.timedelta(days=delta)
        self.d = self.date.day
        self.m = self.date.month
        self.y = self.date.year
        self.dateText = str(self.d)+"."+str(self.m)+"."+str(self.y)

class simpleSession(object):
	"""docstring for simpleSession"""
	def __init__(self, id):
		self.timeWait = False
		self.contactWait=False
		self.editWait = False
		self.loginWait = True
		self.name = ""
		self.id = id
		self.time = datetime.datetime.now().day
		
sessions = {}

time = []
time.append(simpleTime(0))
try:
	time.append(simpleTime(1))
except Exception as e:
	print(e)
try:
	time.append(simpleTime(2))
except Exception as e:
	print(e)

def updateTime():
	time[0] = simpleTime(0)
	try:
		time[1] = simpleTime(1)
	except Exception as e:
		print(e)
	try:
		time[2] = simpleTime(2)
	except Exception as e:
		print(e)


def search(name, cel):
	s = 0
	temp = name
	temp = temp.lower()
	temp = temp.split(' ')
	#print(temp)
	n = cel.lower()
	n = n.split(' ')
	for k in n:
		for j in temp:
			if (k == j):
				s+=1
	if (s>=1):
		return True 
	else:
		return False

def getDashboard(name, day):
	rb = xlrd.open_workbook('/home/dima/CRM/График.xlsx')
	sheet = rb.sheet_by_index(0)
	rowNum = 0
	a1 = sheet.cell_value(rowx=row_DAY, colx=col_FIO)
	fl = False
	i = 0
	while fl == False and i < 36:
		temp = sheet.cell_value(i, col_FIO)
		if temp!='':
			fl = search(name, temp)
		if (fl == True):
			rowNum = i
		i+=1
	#print(rowNum)
	rowNumEx = rowNum
	rowZone = 1
	a1 = sheet.cell_value(rowNum + 1, col_FIO)
	while (a1 == ''):
		rowZone += 1
		rowNum += 1
		a1 = sheet.cell_value(rowNum + 1, col_FIO)
	#print(rowZone)
	#colNum = getCol(float(day))
	day = float(day)
	colNum = 0
	a1 = sheet.cell_value(row_DAY, colx=0)
	for i in range(0,34):
        	temp = sheet.cell_value(2, i)
        	if (temp == day):
            		colNum = i
	if (fl == True):
		result = "Сотрудник не в смене"
	else:
		result = "Сотрудник не найден"
	tempRes = (0,0)
	for i in range(0,rowZone):
		if (sheet.cell(rowNumEx+i, colNum).value !=''):
			if (sheet.cell(rowNumEx+i, colNum).value !='Отпуск'):
				result = "Работает:\n"+sheet.cell(rowNumEx+i, colNum).value + "\nGMT +4 (Самара)"
			else:
				result = "Сотрудник в отпуске"
	return result


def makeEdit(value):
	rb = xlrd.open_workbook('/home/dima/CRM/График.xlsx')
	wb = xlcopy(rb)
	wr_sheet = wb.get_sheet(0) 
	sheet = rb.sheet_by_index(0)
	rowNum = 0
	a1 = sheet.cell_value(rowx=row_DAY, colx=col_FIO)
	fl = False
	i = 0

	data = value.split()
	name = data[0]
	day = data[1]
	start = data[2]
	end = data[3]

	while fl == False and i < 36:
		temp = sheet.cell_value(i, colx=col_FIO)
		if temp!='':
			fl = search(name, temp)
		if (fl == True):
			rowNum = i
		i+=1
	#print(rowNum)
	rowNumEx = rowNum
	rowZone = 1
	a1 = sheet.cell_value(rowNum + 1, colx=col_FIO)
	while (a1 == ''):
		rowZone += 1
		rowNum += 1
		a1 = sheet.cell_value(rowNum + 1, colx=col_FIO)
	#print(rowZone)
	#colNum = getCol(float(day))
	day = float(day)
	colNum = 0
	a1 = sheet.cell_value(row_DAY, colx=0)
	for i in range(0,34):
        	temp = sheet.cell_value(2, i)
        	if (temp == day):
            		colNum = i
	if (fl == True):
		result = "Сотрудник не в смене"
	else:
		result = "Сотрудник не найден"
	tempRes = (0,0)
	wr_sheet.write(rowNumEx, colNum, str(start)+":00 - "+str(end)+":00")
	wb.save('/home/dima/CRM/График.xlsx')
	return "Корректировка - успешно"





#getDashboard('тюшняков','22')


