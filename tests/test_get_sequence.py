import unittest
import os
import pathlib

from nussinov.nussinov import getSequence

class TestGetSequence(unittest.TestCase):

    def setUp(self):
        from argparse import Namespace
        self.args = Namespace(sequence=None, filepath=None)

    def test_none(self):
        self.assertEqual(getSequence(self.args), None)

    def test_sequence_string(self):
        self.args.sequence = "GCAU"
        self.assertEqual(getSequence(self.args), self.args.sequence)

    def test_filepath(self):
        self.args.filepath = os.path.join(pathlib.Path().absolute(), 'tests', 'test_filepath.txt')
        print(self.args.filepath)
        self.assertEqual(getSequence(self.args), "GCAU")
    
    def test_bad_filepath(self):
        self.args.sequence = None
        self.args.filepath = 'file_not_found.txt'
        self.assertEqual(getSequence(self.args), None)

if __name__ == '__main__':
    unittest.main()