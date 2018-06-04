#!/usr/bin/python3

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine.url import URL


class Connexion:

	def connect(self,drivername,username= 'postgres', password='ifsttar', host='137.121.74.24',port='5432',database='maps'):
		print("on est dans connexion")
        # engine = create_engine('postgresql://postgres:ifsttar@137.121.74.24:5432/maps',echo=True,client_encoding='utf8')
		try:    	
			url = URL(drivername, username=username, password=password, host=host, port=port, database=database)
			engine = create_engine(url, echo=True, client_encoding='utf8')

			engine.connect()
			Session = sessionmaker(bind=engine)
			session = Session()
			metadata = MetaData(engine)
			conn = engine.connect()

			return conn, session, engine, metadata
		except OperationalError as oe:
			print(oe.reason+" bah on ne sait pas")

	def disconnect(self,conn, session, engine):
		print("on est dans déconnexion")
		session.close()
		conn.close()
		engine.dispose()