
import unittest
from TestUtils import TestUtils
import inspect

class TestSymbolTable(unittest.TestCase):

    def test_000(self):
        input = ["INSERT x number", "INSERT y string"]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 100)) 
    def test_000(self):
        input = ["BEGIN",
                 "INSERT x string",
                 "BEGIN",
                 "INSERT x number",
                 "ASSIGN x x",
                 "END",
                 "END"]
        expected = ["success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 100)) 
    def test_002(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "INSERT x string"
        ]
        expected = ["Redeclared: INSERT x string"]
        self.assertTrue(TestUtils.check(input, expected, 102))


    def test_003(self):
        input = ["BEGIN","BEGIN","END","END"]
        expected = [""]
        self.assertTrue(TestUtils.check(input, expected, 103)) 
    
    def test_004(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x 15",
            "ASSIGN y 17",
            "ASSIGN x 'abc'",
        ]
        expected = ["TypeMismatch: ASSIGN y 17"]
        self.assertTrue(TestUtils.check(input, expected, 104))


    def test_005(self):
        input = [
            "PRINT",
            "INSERT x number",
            "PRINT",
        ]
        expected = ["", "success", "x//0"]
        self.assertTrue(TestUtils.check(input, expected, 105)) 
    
    def test_006(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "END",
            "END"
        ]
        expected = ["success", "success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 106))

    def test_007(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "END",
        ]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, 107))
    
    
    def test_008(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "LOOKUP x",
            "LOOKUP y",
            "END"
        ]
        expected = ["success", "success", "success", "1", "0"]
        self.assertTrue(TestUtils.check(input, expected, 108))


    def test_009(self):
        input = [
            "INSERT x number",
            "ASSIGN x y",
        ]
        expected = ["Undeclared: ASSIGN x y"]
        self.assertTrue(TestUtils.check(input, expected, 109)) 

    def test_010(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "PRINT",
            "END"
        ]
        expected = ["success", "success", "success", "success", "y//0 x//1 z//1"]
        self.assertTrue(TestUtils.check(input, expected, 110))

    
    def test_011(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x y",
        ]
        expected = ["TypeMismatch: ASSIGN x y"]
        self.assertTrue(TestUtils.check(input, expected, 111))

    def test_012(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "RPRINT",
            "END"
        ]
        expected = ["success", "success", "success", "success", "z//1 x//1 y//0"]
        self.assertTrue(TestUtils.check(input, expected, 112))
 

    def test_013(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "END",
            "END",
        ]
        expected = ["success", "success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 113)) 

    def test_014(self):
        input = [
            "END",
        ]
        expected = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(input, expected, 114)) 

    def test_015(self):
        input = [
            "INSERT 1abc number"
        ]
        expected = ["Invalid: INSERT 1abc number"]
        self.assertTrue(TestUtils.check(input, expected, 115))


    def test_016(self):
        input = [
            "BEGIN",
        ]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, 116)) 
    
    def test_017(self):
        input = [
            "BEGIN",
            "BEGIN",
            "END",
            "BEGIN",
        ]
        expected = ["UnclosedBlock: 2"]
        self.assertTrue(TestUtils.check(input, expected, 117)) 
    
    def test_018(self):
        input = [
            "INSERT x string",
            "ASSIGN x 'ab@'"
        ]
        expected = ["Invalid: ASSIGN x 'ab@'"]
        self.assertTrue(TestUtils.check(input, expected, 118))

    def test_019(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "LOOKUP x",
            "LOOKUP y",
            "END",
        ]
        expected = ["success", "success", "success", "1", "0"]
        self.assertTrue(TestUtils.check(input, expected, 119)) 

    def test_020(self):
        input = [
            "BEGIN",
            "INSERT x number"
        ]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, 120))

    def test_021(self):
        input = [
            "LOOKUP x"
        ]
        expected = ["Undeclared: LOOKUP x"]
        self.assertTrue(TestUtils.check(input, expected, 121))

    def test_022(self):
        input = [
            "INSERT x number",
            "INSERT y number",
            "ASSIGN x y"
        ]
        expected = ["success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 122))

    def test_023(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT z number",
            "ASSIGN x 123",
            "LOOKUP x",
            "LOOKUP z",
            "BEGIN",
            "INSERT y string",
            "LOOKUP y",
            "END",
            "LOOKUP y",
            "END",
        ]
        expected = ["success", "success", "success", "success", "0", "1", "success", "2", "0"]
        self.assertTrue(TestUtils.check(input, expected, 123))

    def test_024(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "BEGIN",
            "INSERT z number",
            "PRINT",
            "END",
            "RPRINT",
            "END",
            "LOOKUP x"
        ]
        expected = ["success", "success", "success", "x//0 y//1 z//2", "y//1 x//0", "0"]
        self.assertTrue(TestUtils.check(input, expected, 124))

    def test_025(self):
        input = [
            "INSERT s string",
            "ASSIGN s 'abc"
        ]
        expected = ["Invalid: ASSIGN s 'abc"]
        self.assertTrue(TestUtils.check(input, expected, 125))

    def test_026(self):
        input = [
            "INSERT x number",
            "ASSIGN x 123a"
        ]
        expected = ["Invalid: ASSIGN x 123a"]
        self.assertTrue(TestUtils.check(input, expected, 126))

    def test_027(self):
        input = [
            "LOOKUP"
        ]
        expected = ["Invalid: LOOKUP"]
        self.assertTrue(TestUtils.check(input, expected, 127))

    
    def test_028(self):
        input = [
            "PRINT abc"
        ]
        expected = ["Invalid: PRINT abc"]
        self.assertTrue(TestUtils.check(input, expected, 128))


    def test_029(self):
        input = [
            "",
            "INSERT x number"
        ]
        expected = ["Invalid: "]
        self.assertTrue(TestUtils.check(input, expected, 129))
    
    def test_030(self):
        input = [
            "INSERT vt_ltnc",
            "BEGIN"
        ]
        expected = ["Invalid: INSERT vt_ltnc"]
        self.assertTrue(TestUtils.check(input, expected, 131))


    def test_031(self):
        input = [
            "LOOKUP 1",
            "BEGIN"
        ]
        expected = ["Invalid: LOOKUP 1"]
        self.assertTrue(TestUtils.check(input, expected, 132))

    def test_032(self):
        input = [
            "BEGIN 1",
            "BEGIN"
        ]
        expected = ["Invalid: BEGIN 1"]
        self.assertTrue(TestUtils.check(input, expected, 133))


    def test_033(self):
        input = [
            "BBEGIN",
            "BEGIN"
        ]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, 134))

    def test_034(self):
        input = [
            "INSERT a number "
        ]
        expected = ["Invalid: INSERT a number "]
        self.assertTrue(TestUtils.check(input, expected, 135))

    
    def test_035(self):
        input = [
            "INSERT  a number"
        ]
        expected = ["Invalid: INSERT  a number"]
        self.assertTrue(TestUtils.check(input, expected, 136))

    def test_036(self):
        input = [
            "INSERT a string",
            "INSERT A string"
        ]
        expected = ["Invalid: INSERT A string"]
        self.assertTrue(TestUtils.check(input, expected, 137))
    
    def test_037(self):
        input = [
            "BEGIN",
            "END"
        ]
        expected = [""]
        self.assertTrue(TestUtils.check(input, expected, 138))
    
    def test_038(self):
        input = [
            "INSERT a number",
            "BEGIN",
            "INSERT a string",
            "ASSIGN a 1",
            "END"
        ]
        expected = ["TypeMismatch: ASSIGN a 1"]
        self.assertTrue(TestUtils.check(input, expected, 139))

    def test_039(self):
        input = [
            "INSERT a number", 
            "BEGIN", 
            "INSERT a string", 
            "LOOKUP a", 
            "END"
        ]
        expected = ["success", "success", "1"]
        self.assertTrue(TestUtils.check(input, expected, 140))

    def test_040(self):
        input = [
            "INSERT a number", 
            "BEGIN", 
            "INSERT a number", 
            "LOOKUP a", 
            "END"
        ]
        expected = ["success", "success", "1"]
        self.assertTrue(TestUtils.check(input, expected, 141))

    def test_041(self):
        input = [
            "INSERT y string",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y y",
            "END"
        ]
        expected = ["success","success","success"]
        self.assertTrue(TestUtils.check(input, expected, 142))

    def test_042(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT x string",
            "BEGIN",
            "INSERT x number",
            "ASSIGN x x",
            "END",
            "END"
        ]
        expected = ["success","success","success","success"]
        self.assertTrue(TestUtils.check(input, expected, 143))

    def test_043(self):
        input = [
            "INSERT x AAAAA"
        ]
        expected = ["Invalid: INSERT x AAAAA"]
        self.assertTrue(TestUtils.check(input, expected, 144))

    def test_044(self):
        input = [
            "ASSIGN x 1AAAA"
        ]
        expected = ["Invalid: ASSIGN x 1AAAA"]
        self.assertTrue(TestUtils.check(input, expected, 145))

    def test_045(self):
        input = [
            "INSERT string number"
        ]
        expected = ["success"]
        self.assertTrue(TestUtils.check(input, expected, 146))

    def test_046(self):
        input = [
            "BEGIN",
            "BEGIN",
            "END",
            "END",
            "END"
        ]
        expected = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(input, expected, 147))

    def test_047(self):
        input = [
            "PRINT",
        ]
        expected = [""]
        self.assertTrue(TestUtils.check(input, expected, 148))

    def test_048(self):
        input = [
            "RPRINT",
        ]
        expected = [""]
        self.assertTrue(TestUtils.check(input, expected, 149))

    def test_049(self):
        input = [
            "INSERT x number",
            "INSERT y number",
            "INSERT z number",
            "BEGIN",
            "INSERT x number",
            "INSERT y number",
            "INSERT z number",
            "PRINT",
            "END",
            "INSERT t string",
            "RPRINT"
        ]
        expected = ['success', 'success', 'success', 'success', 'success', 'success', 'x//1 y//1 z//1', 'success', 't//0 z//0 y//0 x//0']
        self.assertTrue(TestUtils.check(input, expected, 1))

    def test_050(self):
        input = [
            "INSERT x number",
            "INSERT y number",
            "INSERT z number",
            "BEGIN",
            "INSERT x number",
            "INSERT y number",
            "INSERT z number",
            "PRINT",
            "END",
            "INSERT t string",
            "RPRINT"
        ]
        expected = ['success', 'success', 'success', 'success', 'success', 'success', 'x//1 y//1 z//1', 'success', 't//0 z//0 y//0 x//0']
        self.assertTrue(TestUtils.check(input, expected, 151))

    

    

    

    