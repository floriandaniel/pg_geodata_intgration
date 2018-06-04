#!/usr/bin/python3

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine.url import URL

class Database:

    def createDatabase(self,url,name_database):
        driver = url['driver']
        username = url['username']
        password = url['password']
        host = url['host']
        port = url['port']
        database = name_database

        link = "{}://{}:{}@{}:{}/{}".format(driver,username,password,host,port,database)
        
        if not database_exists(link):
            create_database(link)
        else:
            print("Error")
    

    def dropDatabase():
        print("on est dans déconnexion")
        session.close()
        conn.close()
        engine.dispose()