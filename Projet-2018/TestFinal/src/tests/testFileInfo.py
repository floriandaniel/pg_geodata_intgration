#!/usr/bin/python3

import unittest
from nose.tools import assert_equal,assert_raises,raises
from parameterized import parameterized
from src.pre_processing.fileInfo import real_file,file_name,file_size,file_extension,file_count_sheets

class FileInfoTestCase(unittest.TestCase):
    
    @parameterized.expand([
        ("faux","-comunes.xls"),
        ("faux","../../-comunes.xls"),
    ])
    
    def test_real_fileException(self,_, a):
        assert_raises(FileNotFoundError, real_file,a)


    @parameterized.expand([
        ("1","res/excels/gaz-communes.xls",True),
        ("2","res/others/README.pdf",True),
        ("3","res/others/diapo.odp",True),
    ])
    
    def test_Real_File(self,_, a,oracle):
        assert_equal(real_file(a),oracle)



    @parameterized.expand([
        ("1","res/excels/gaz-communes.xls","gaz-communes.xls"),
        ("2","res/others/README.pdf","README.pdf"),
        ("3","res/others/diapo.odp","diapo.odp"),
    ])
    
    def test_Name(self,_, a,oracle):
        assert_equal(file_name(a),oracle)


    @parameterized.expand([
        ("1","res/excels/gaz-communes.xls",".xls"),
        ("2","res/others/README.pdf",".pdf"),
        ("3","res/others/diapo.odp",".odp"),
    ])
    
    def test_Extension(self,_, a,oracle):
        assert_equal(file_extension(a),oracle)



    @parameterized.expand([
        ("1","res/excels/gaz-communes.xls",(2307072,'2 MB')),
        ("2","res/img/png/users.png",(15430,'15 KB')),
        ("3","res/geo/types/dbf/42-.dbf",(66010,'64 KB')),
        ("4","res/geo/types/dbf/81-.dbf",(65210,'63 KB')),
    ])
    
    def test_Size(self,arez, a,oracle):
        print("arez = "+str(arez))
        assert_equal(file_size(a),oracle)


    @parameterized.expand([
        ("1","res/excels/gaz-communes.xls",2),
    ])
    
    def test_Sheets(self,_, a,oracle):
        assert_equal(file_count_sheets(a),oracle)
