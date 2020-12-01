import unittest
import random

from nussinov.nussinov import checkSequence

class TestCheckSequence(unittest.TestCase):

    def test_none(self):
        sequence = None
        self.assertFalse(checkSequence(sequence))

    def test_single_character(self):
        sequence = "G"
        self.assertTrue(checkSequence(sequence))

    def test_bad_single_character(self):
        sequence = "B"
        self.assertFalse(checkSequence(sequence))
    
    def test_long_sequence(self):
        sequence = ''.join(random.choice(['G','C','U', 'A']) for _ in range(64))
        self.assertTrue(checkSequence(sequence))

    def test_bad_long_sequence(self):
        sequence = ''.join(random.choice(['G','C','U', 'A']) for _ in range(64)) + 'F'
        self.assertFalse(checkSequence(sequence))
        sequence = 'S'.join(random.choice(['G','C','U', 'A']) for _ in range(64))
        self.assertFalse(checkSequence(sequence))
        sequence = ''.join(random.choice(['G','C','U', 'A']) for _ in range(64))
        index = random.randint(0, 63)
        sequence = sequence[:index] + 'F' + sequence[index:]
        self.assertFalse(checkSequence(sequence))

if __name__ == '__main__':
    unittest.main()