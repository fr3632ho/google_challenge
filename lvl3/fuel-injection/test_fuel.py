import unittest
import fuel as f

class FuelTest(unittest.TestCase):

    @staticmethod
    def sol(n):
        return f.solution(n)

    def test_small_numbers(self):
        self.assertTrue('2' == FuelTest.sol('4'))

        self.assertTrue('5' == FuelTest.sol('15'))

        self.assertTrue('6' == FuelTest.sol('33'))

    def test_larger_one(self):
        self.assertTrue('25' == FuelTest.sol('33554432'))

        self.assertTrue('26' == FuelTest.sol('33554433'))


    def test_larger_two(self):
        self.assertTrue('35' == FuelTest.sol('34359738368'))

        self.assertTrue('36' == FuelTest.sol('34359738369'))


    '''
    Need more precision for numbers greater than 32 bits
    '''
    def test_larger_three(self):
        self.assertTrue('65' == FuelTest.sol('36893488147419103232'))

        # Not precise enough since log2(36893488147419103233) drops the decimals
        # log2(36893488147419103233) := 65.00000000000000000003910432743914694440847769453274735744
        self.assertTrue('66' == FuelTest.sol('36893488147419103233'))

    '''
    Need more precision
    '''
    def test_huge_one(self):
        self.assertTrue('128' == FuelTest.sol(('340282366920938463463374607431768211456')))

        # Not precise enough
        self.assertTrue('129' == FuelTest.sol(('340282366920938463463374607431768211457')))





if __name__ == "__main__":
    unittest.main()
