#!/usr/bin/python3
import unittest
from nose.tools import assert_equal,assert_raises,raises
from check_kwargs import is_correct_kwargs,allo
from parameterized import parameterized,param
from exceptions import ValueNotMatchOption,OptionNotFound,FolderAlreadyExists
from utils.folder import create_dir
# from utils.check_kwargs import is_correct_kwargs

from shutil import rmtree
from os.path import isdir
import os

class UtilsTestCase(unittest.TestCase):



    @parameterized.expand([
        ("Test Kwargs",{'inter':['marché','flora'],'va':['llée','mos']},{'inte':'marché'}),
    ])
    
    def test_Test_KwargsException1(self,_,a,b):
        assert_raises(OptionNotFound,is_correct_kwargs,a,b)

    def test_Test_KwargsException(self):
        assert_raises(ValueNotMatchOption,allo)

            # @parameterized.expand([
    #     ("CurrentRepo","gaz-communes.xls",True),
    #     ("RelativePath","../README.pdf",True),
    #     ("AbsPath","/home/florian-stage/Téléchargements/diapo.odp",True),
    # ])
    
    # def test_create_dir(self,_, a,oracle):
    #     assert_equal(real_file(a),oracle)

    
    try :
        rmtree("/srv/geodata/aaal")
        rmtree("/srv/geodata/allo")
    except FileNotFoundError:
        pass



    dir_path = "/srv/geodata/test_directory"
    if not isdir(dir_path) :
            os.makedirs(dir_path)
    else :
        print("Veuillez trouver un autre nom, ou supprimez le dossier.")


    @parameterized.expand([
        ("Value Option Error 1","/srv/geodata/aaal","errror"),
        ("Value Option Error 2","/srv/geodata/allo","errordddd"),
        ("Value Option Error 3","/srv/geodata/allo","econtinue"),
    ])
    
    def test_create_dirException(self,_, a,if_exists):
        assert_raises(ValueNotMatchOption, create_dir,a,if_exists=if_exists)



    @parameterized.expand([
        ("Typing Error 1","/srv/geodata/aaal","error"),
        ("Typing Error 2","/srv/geodata/allo","error"),
    ])
    
    def test_create_dirException(self,_, a,if_exists):
        assert_raises(OptionNotFound, create_dir,a,if_exis=if_exists)

    @parameterized.expand([
        ("Folder Exists 1",dir_path,"error"),
    ])
    
    def test_create_dirException(self,_, a,if_exists):
        assert_raises(FolderAlreadyExists, create_dir,a,if_exists=if_exists)


    @parameterized.expand([
        ("Folder Exists 1",dir_path,"error"),
    ])
    
    def test_create_dirException(self,_, a,b):
        assert_raises(FolderAlreadyExists, create_dir,a,if_exists=b)
