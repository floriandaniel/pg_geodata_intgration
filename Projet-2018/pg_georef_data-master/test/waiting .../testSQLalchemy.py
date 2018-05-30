# #!/usr/bin/python3
from sqlalchemy import *
from sqlalchemy.orm import *
from patoolib import extract_archive, test_archive
from patoolib.util import PatoolError

engine = create_engine('postgresql://postgres:ifsttar@137.121.74.24:5432/maps')

# db_name = "test"
# engine.execute("CREATE DATABASE {}".format("db")).execution_options(isolation_level="AUTOCOMMIT")
# # conn.execute("CREATE DATABASE %s  ;" % db_name)

# create a database connection
engine.connect()

# res = engine.execute("select 1 as is_alive;")
metadata = MetaData(engine)
# print(str(res))
# print(metadata.tables.keys())	
village_table = Table('village',metadata,schema="dpt",autoload=True)


# create an Insert object
ins = village_table.insert()
# add values to the Insert object
new_village = ins.values(abc="Joe")
 
conn = engine.connect()
# add user to database by executing SQL
conn.execute(new_village)




# Vérifie si un fichier est une archive
# @param String file path

# @return bool
# @return string caption

def is_compressed(file_path) :
	try :
		res = test_archive("fichiers shape.zip", verbosity=-1, interactive=False)
	except PatoolError :
		return False,"the file is not an archive or not correctly defined"
	return True,"the file is an archive"



# -------TESTS BASIQUES-------
res,string = is_compressed("fichiers shape.zip")
print(res)
print(string)



# -------INFO FILE-------
file = open("foot.txt","wt")
file.db_name

>>> magic.from_file('greenland.png', mime=True)
'image/png'

os.path.getsize(path)
os.path.basename(path) 