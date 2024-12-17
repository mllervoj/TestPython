from DataProcessing import *
import unittest

class TestDataProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        file = "test_pohovor_uloha_python/223344.xlsx"
        self.process = DataProcessing(file)

    def test_rowCount(self):
        self.assertEqual(self.process.rowCount(), 23)

    def test_columnCount(self):
        self.assertEqual(self.process.columnCount(), 14)

    def test_uniqueColumnCount(self):
        self.assertEqual(self.process.uniqueColumnCount('Výsledek'), 3)

    def test_emptyColumnCount(self):
        self.assertEqual(self.process.emptyColumnCount('TAB'), 2)

    def test_meanColumn(self):
        self.assertAlmostEqual(self.process.meanColumn('Délka'), 129.19, 3)

    def test_minColumn(self):
        self.assertEqual(self.process.minColumn('Délka'), 1.5)

    def test_maxColumn(self):
        self.assertEqual(self.process.maxColumn('Délka'), 1900.4)

if __name__=='__main__':
    unittest.main()