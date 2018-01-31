import unittest
import gcodelib.moves as moves

class TestMove(unittest.TestCase):
    def setUp(self):
        self.move = moves.Move(x=1, y=1.2, z=3.141789)
        self.move.code = "TST"
        
    def test_str(self):
        self.assertEqual(str(self.move),"TST X1.000 Y1.200 Z3.142")

class TestRapid(unittest.TestCase):
    def test_rapid(self):
        self.assertEqual(str(moves.Rapid(x=2, y=3.5)),"G00 X2.000 Y3.500")
        self.assertEqual(str(moves.Rapid(z=5, f=400)),"G00 Z5.000 F400.000")

class TestLine(unittest.TestCase):
    def test_line(self):
        self.assertEqual(str(moves.Line(x=2, y=3.5)),"G01 X2.000 Y3.500")
        self.assertEqual(str(moves.Line(z=5, f=400)),"G01 Z5.000 F400.000")

class TestArc(unittest.TestCase):
    def test_clockwise_arc(self):
        self.assertEqual(str(moves.Arc(x=1, y=2.5, i=3, j=4.5, clockwise=True)), "G02 X1.000 Y2.500 I3.000 J4.500")
        
    def test_anticlockwise_arc(self):
        self.assertEqual(str(moves.Arc(x=1, y=2.5, i=3, j=4.5, clockwise=False)), "G03 X1.000 Y2.500 I3.000 J4.500")        
