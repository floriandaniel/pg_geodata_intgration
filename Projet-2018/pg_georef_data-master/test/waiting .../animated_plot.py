# #!/usr/bin/python3
import psycopg2
from urllib.request import urlretrieve
import xlrd
import csv

# import sys

# if sys.version_info[0] < 3:
# 	import Tkinter as tk
# else:
#   	import tkinter as tk



# root = tk.Tk()
# path = "memory.png"
# img = ImageTk.PhotoImage(Image.open(path))
# panel = tk.Label(root, image = img)
# panel.pack(side = "bottom", fill = "both", expand = "yes")
# root.mainloop()

# #!/usr/bin/python3
 
database = "azerty"
table = "t"
schema = "xcvbn"

SIZE_MEMORY = 50

conn = psycopg2.connect(host="137.121.74.24",database="maps", user="postgres", password="ifsttar")
cur = conn.cursor()
query = "SELECT pg_size_pretty(pg_database_size('{}'))"
cur.execute(query.format("maps"))
result = cur.fetchone()
print("Taille de la base de données : ",result[0])



query2 = "SELECT pg_size_pretty(pg_total_relation_size('{}'))"
cur.execute(query2.format("dpt.loire"))
result = cur.fetchone()
print("Taille de la table : ",result[0])


query3 = "SELECT reltuples AS approximate_row_count FROM pg_class WHERE relname = '{}'"
cur.execute(query3.format("loire"))
result = cur.fetchone()
print("Approximation du nombre de lignes : ",result[0])



query4 = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS where table_name='{}'"
cur.execute(query4.format("loire"))
result = cur.fetchone()
print("Nombre de colonnes : ",result[0])

conn.close()

# urlretrieve('http://www.statistiques.developpement-durable.gouv.fr/fileadmin/documents/Themes/Energies_et_climat/Les_differentes_energies/Electricite/enquete_livraison/2013/livraison-electricite-2013-communes-b.xls', "commune.xls")
# urlretrieve('http://www.statistiques.developpement-durable.gouv.fr/fileadmin/documents/Themes/Energies_et_climat/Les_differentes_energies/Electricite/enquete_livraison/livraison-electricite-2012-communes.xls', "commune1.xls")



# csvActivite = urllib.request.urlopen("")
# csvActiviteOld = open("hello.xls","w")
# csvActiviteOld.write(csvActivite.read().decode("utf-8"))
# csvActivite.close()
# csvActiviteOld.close()
# urlretrieve('http://www.statistiques.developpement-durable.gouv.fr/fileadmin/documents/Themes/Energies_et_climat/Les_differentes_energies/Gaz_naturel/enquete_livraison/2014/livraison-gaz-2014-communes.xls','gaz-communes.xls')


import pandas as pd
xls = pd.ExcelFile('copie.xls')
df = xls.parse(sheet_name="Variables", index_col=None, na_values=['NA'])
df.to_csv('file.csv')





# http://www.statistiques.developpement-durable.gouv.fr/fileadmin/documents/Themes/Energies_et_climat/Les_differentes_energies/Electricite/enquete_livraison/2013/livraison-electricite-2013-communes-b.xls










	

















# import matplotlib
# matplotlib.use('TkAgg')

# from numpy import arange, sin, pi
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure




# def destroy(e):
#     sys.exit()

# root = Tk.Tk()
# root.wm_title("Embedding in TK")


# f = Figure(figsize=(5, 4), dpi=100)
# a = f.add_subplot(111)
# t = arange(0.0, 3.0, 0.01)
# s = sin(2*pi*t)

# a.plot(t, s)
# a.set_title('Tk embedding')
# a.set_xlabel('X axis label')
# a.set_ylabel('Y label')


# # a tk.DrawingArea
# canvas = FigureCanvasTkAgg(f, master=root)
# canvas.draw()
# canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

# canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

# button = Tk.Button(master=root, text='Quit', command=sys.exit)
# button.pack(side=Tk.BOTTOM)

# Tk.mainloop()