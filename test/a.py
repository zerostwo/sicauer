import xlrd

data = xlrd.open_workbook('a.xls')
table = data.sheets()[0]
print(table)