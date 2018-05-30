import unittest
from nose.tools import assert_equal,assert_raises,raises
from parameterized import parameterized
from pre_processing.fileInfo import real_file,file_name,file_size,file_extension,file_count_sheets

class FileInfoTestCase(unittest.TestCase):
    
    @parameterized.expand([
        ("faux","-comunes.xls"),
        ("faux","../../-comunes.xls"),
    ])
    
    def test_real_fileException(self,_, a):
        assert_raises(FileNotFoundError, real_file,a)


    @parameterized.expand([
        ("CurrentRepo","files/excels/gaz-communes.xls",True),
        ("RelativePath","files/others/README.pdf",True),
        ("AbsPath","files/others/diapo.odp",True),
    ])
    
    def test_real_file(self,_, a,oracle):
        assert_equal(real_file(a),oracle)



    @parameterized.expand([
        ("CurrentRepo","files/excels/gaz-communes.xls","gaz-communes.xls"),
        ("RelativePath","files/others/README.pdf","README.pdf"),
        ("AbsPath","files/others/diapo.odp","diapo.odp"),
    ])
    
    def test_file_name(self,_, a,oracle):
        assert_equal(file_name(a),oracle)


    @parameterized.expand([
        ("CurrentRepo","files/excels/gaz-communes.xls",".xls"),
        ("RelativePath","files/others/README.pdf",".pdf"),
        ("AbsPath","files/others/diapo.odp",".odp"),
    ])
    
    def test_file_extension(self,_, a,oracle):
        assert_equal(file_extension(a),oracle)


    @parameterized.expand([
        ("CurrentRepo","files/excels/gaz-communes.xls",2),
    ])
    
    def test_file_extension(self,_, a,oracle):
        assert_equal(file_count_sheets(a),oracle)
