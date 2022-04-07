'''

Test module for gcd
'''

import unittest
from gcd import gcd


class TestGcd(unittest.TestCase):
    '''
    Test Class
    '''

    def test_result(self):
        '''
        Testing correct result
        '''
        self.assertAlmostEqual(gcd(18, 12), 6)
        self.assertAlmostEqual(gcd(13, 5), 1)
        self.assertAlmostEqual(gcd(6, 21), 3)

    def test_types(self):
        '''
        Make sure type errors are raised
        '''
        self.assertRaises(TypeError, gcd, 2+1j, 42)
        self.assertRaises(TypeError, gcd, '42', 42)
        self.assertRaises(TypeError, gcd, True, 42)
        self.assertRaises(TypeError, gcd, [42], 42)

    def test_values(self):
        '''
        Make sure value errors are raised
        '''
        self.assertRaises(ValueError, gcd, -112, 42)


if __name__ == '__main__':
    # bash: python -m unittest test_gcd.py
    # -or_: python -m unittest

    unittest.main()
