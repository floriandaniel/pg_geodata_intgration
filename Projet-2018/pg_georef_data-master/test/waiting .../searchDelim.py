# #!/usr/bin/python3
import re
import xlrd
import pandas as pd
import csv

monDictionnaire = {}
monDictionnaire["\""] = 5

for key in monDictionnaire.keys() :
	if key == "\"":
		monDictionnaire["\""] += 1
print(monDictionnaire)


# xls = pd.ExcelFile('copie.xls')
# df = xls.parse(sheet_name="Variables", index_col=None, na_values="NaN")
# df.to_csv('file.csv')

workbook = xlrd.open_workbook('copie.xls', formatting_info=False)
for sh in workbook.sheets():
	print(sh.name, sh.nrows, sh.ncols)
	for column in range(sh.ncols) :
		cpt = 0
		for row in range(sh.nrows) :
			cell = sh.cell(row,column)
					
			ctype = cell.ctype
			# print(ctype)
			if ctype in( xlrd.XL_CELL_EMPTY,xlrd.XL_CELL_BLANK ):
				# print("ERROR")
				cpt+=1
		print("Compteur : ",cpt,"// Lignes max : ",sh.nrows)
		if cpt == sh.nrows :
			print("colonne nulle numero",column)


# df=pd.read_csv('file.csv')
# df=df.dropna()


fname_in = 'file.csv'
fname_out = 'fileOut.csv'

with open(fname_in, 'rt') as fin, open(fname_out, 'wt') as fout:
	reader = csv.reader(fin)
	writer = csv.writer(fout)
	compteur = 0
	for row in reader:
		print(row[1])
		if compteur not in {0,1,13,5,6} :
			# del row
			# print("OK ou KO")
			writer.writerow(row)
		compteur+=1


arrayofvalues = sh.col_values(sh.ncols-1)
print("Array of Values : "+str(arrayofvalues))
password = ":"
low = re.search(r"[a-zA-Z][0-9][\"\']", password)
# 
# up = re.search(r"", password)
# num = re.search(r"", password)
# has_all = all((low, up, num))
print(str(low))

if low != None : 
	print("Oui")
else : 
	print('Dead')