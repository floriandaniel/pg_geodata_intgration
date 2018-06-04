#!/usr/bin/python3
import unittest
from nose.tools import assert_equal,assert_raises,raises
from parameterized import parameterized,param
from shutil import rmtree
from os.path import isdir
import os
import sys
import io
from contextlib import redirect_stdout


from src.utils.exceptions import ValueNotMatchOption,OptionNotFound,FolderAlreadyExists
from src.utils.folder import create_dir
from src.utils.check_kwargs import is_correct_kwargs,foo






class UtilsTestCase(unittest.TestCase):

    def init() :
        """On prépare l'environnement avant les tests :
        création de dossiers,
        suppression de fichiers, ..
        """

        try :
            rmtree("/srv/geodata/aaal")
            rmtree("/srv/geodata/allo")
        except FileNotFoundError:
            pass

        global dirs_paths
        global dirs_paths_uncreated 
        dirs_paths = ["/srv/geodata/test_directory","/srv/geodata/toto","/srv/geodata/tata"]
        dirs_paths_uncreated = ["/srv/geodata/tutu","/srv/geodata/titi"]
        for folder in dirs_paths :   
            if not isdir(folder) :
                    os.makedirs(folder)
            else :
                print("Veuillez trouver un autre nom, ou supprimez le dossier.")


#    def exit() :




    init()



    # IS_CORRECT_KWARGS

    @parameterized.expand([
        ("Test Kwargs",{'inter':['marché','flora'],'va':['llée','mos']},{'inte':'marché'}),
        ("Test Kwargs",{'etat':['ok','ko'],'va':['llée','mos']},{'inte':'marché'}),
        ("Test Kwargs",{'inter':['marché','flora'],'va':['llée','mos']},{'inte':'marché'}),
    ])
    
    def test_Test_KwargsException1(self,_,a,b):
        assert_raises(OptionNotFound,is_correct_kwargs,a,b)

    @parameterized.expand([
        ("Test Kwargs",{'etat':['ok','ko']},{'etat':'null'}),
        ("Test Kwargs",{'fruits':['strawberry','apple']},{'fruits':'orange'}),
    ])

    def test_Test_KwargsException(self,_,oracle_test,test):
        assert_raises(ValueNotMatchOption,is_correct_kwargs,oracle_test,test)



    # CREATE_DIR
    # @parameterized.expand([
    #     ("Value Option Error 1","/srv/geodata/aaal","errror"),
    #     ("Value Option Error 2","/srv/geodata/allo","errordddd"),
    #     ("Value Option Error 3","/srv/geodata/allo","econtinue"),
    # ])
    
    # def test_create_dirException(self,_, a,if_exists):
    #     assert_raises(ValueNotMatchOption, create_dir,a,if_exists=if_exists)



    # @parameterized.expand([
    #     ("Typing Error 1","/srv/geodata/aaal","error"),
    #     ("Typing Error 2","/srv/geodata/allo","error"),
    # ])
    
    # def test_create_dirException1(self,_, a,if_exists):
    #     assert_raises(OptionNotFound, create_dir,a,if_exis=if_exists)
 

    @parameterized.expand([
        ("Folder Exists 1",dirs_paths[0],"error"),
        ("Folder Exists 2",dirs_paths[1],"error"),
    ])
    
    def test_create_dirException2(self,_, a,if_exists):
        assert_raises(FolderAlreadyExists, create_dir,a,if_exists=if_exists)


    @parameterized.expand([
        ("Folder Exists 1",dirs_paths_uncreated[0],"continue","Warning ! Folder is not created, because it already exists."),
        ("Folder Exists 1",dirs_paths_uncreated[1],"continue","Warning ! Folder is not created, because it already exists."),
    ])
    
    def test_create_dirException3(self,_, a,b,oracle):

        f = io.StringIO()
        
        with redirect_stdout(f):
            create_dir(a,if_exists=b)
        output = f.getvalue().rstrip('\n')
 
        assert_equal(output,oracle)



# from io import StringIO

# out = StringIO()
# check_kwargs.foo(out=out)
# output = out.getValue().strip()

# print(output)

    # def test_foo(str):
    #     assert output == 'hello,cccc world!'

    