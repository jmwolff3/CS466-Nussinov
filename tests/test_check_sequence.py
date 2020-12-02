import unittest
import random

from nussinov.nussinov import isSequenceValid

class TestCheckSequence(unittest.TestCase):

    def test_none(self):
        sequence = None
        self.assertFalse(isSequenceValid(sequence))

    def test_single_character(self):
        sequence = "G"
        self.assertTrue(isSequenceValid(sequence))

    def test_bad_single_character(self):
        sequence = "B"
        self.assertFalse(isSequenceValid(sequence))
    
    def test_long_sequence(self):
        sequence = ''.join(random.choice(['G','C','U', 'A']) for _ in range(64))
        self.assertTrue(isSequenceValid(sequence))

    def test_bad_long_sequence(self):
        sequence = ''.join(random.choice(['G','C','U', 'A']) for _ in range(64)) + 'F'
        self.assertFalse(isSequenceValid(sequence))
        sequence = 'S'.join(random.choice(['G','C','U', 'A']) for _ in range(64))
        self.assertFalse(isSequenceValid(sequence))
        sequence = ''.join(random.choice(['G','C','U', 'A']) for _ in range(64))
        index = random.randint(0, 63)
        sequence = sequence[:index] + 'F' + sequence[index:]
        self.assertFalse(isSequenceValid(sequence))

if __name__ == '__main__':
    unittest.main()