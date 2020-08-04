import unittest
from fractions import Fraction
import makrov_chaining as amc

class AmcTest(unittest.TestCase):

    @staticmethod
    def lcm(a, b):
        if a > b:
            greater = a
        else:
            greater = b

        while True:
            if greater % a == 0 and greater % b == 0:
                lcm = greater
                break
            greater += 1

        return lcm

    @staticmethod
    def get_lcm_for(l):
        return reduce(lambda x, y: AmcTest.lcm(x, y), l)

    @staticmethod
    def convert_to_lcd(probs):
        ret = []

        least_common_multiple = AmcTest.get_lcm_for([f.denominator for f in probs])
        for f in probs:
            if f.denominator != least_common_multiple:
                ret.append(Fraction(least_common_multiple / f.denominator * f.numerator, least_common_multiple ) )
            else:
                ret.append(Fraction(f.numerator, least_common_multiple ) )
        return ret

    @staticmethod
    def markov_probabilities(m):
        probs = AmcTest.calculate_b(m)[0]
        return AmcTest.convert_to_lcd(probs)

    @staticmethod
    def calculate_b(m):
        t = amc.transient_count(m)

        if sum(m[0]) == 0:
            terminals = [0 for i in range(len(m) - t - 1)]
            res = [1] + terminals + [1]
            return res

        matrix = amc.sort(m)
        matrix = amc.into_fractions(matrix)

        Q, R = amc.create_QR(matrix, t)
        N = amc.inv(amc.sub(amc.identity(len(Q)), Q))
        M = amc.mul(N, R)
        return amc.mul(N, R)

    def test_fraction(self):
        m = [[0, 2, 1, 0, 0],
             [0, 0, 0, 3, 4],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]

        n = amc.into_fractions(m)
        self.assertTrue( n[0][1] == Fraction(2,3))
        self.assertTrue( n[1][3] == Fraction(3,7))

        b = AmcTest.calculate_b(m)
        b0 = b[0]
        self.assertEqual( Fraction(1,3), b0[0])
        self.assertEqual( Fraction(2,7), b0[1])
        self.assertEqual( Fraction(8,21), b0[2])

    def test_sort(self):
        m = [[1, 1, 3],
                 [0, 0, 0],
                 [3, 1, 2]]
        r = [[1, 3, 1],
                [3, 2, 1],
                [0, 0, 0]]
        self.assertTrue(amc.sort(m) == r)

        m = [[1, 1, 1, 1],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [1, 2, 3, 4]]
        r = [[1, 1, 1, 1],
                [1, 4, 2, 3],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        self.assertTrue(amc.sort(m) == r)

        m = [[0,0], [1,2]]
        r = [[2,1], [0,0]]
        self.assertTrue(amc.sort(m) == r)

        m = [[1,2,3],
             [0,0,0],
             [3,2,1]]
        r = [[1,3,2],
             [3,1,2],
             [0,0,0]]
        self.assertTrue(amc.sort(m) == r)

    def test_result(self):
        # TEST 1
        m = [[0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
             [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
             [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
             [0,0,0,0,0,0],  # s3 is terminal
             [0,0,0,0,0,0],  # s4 is terminal
             [0,0,0,0,0,0]]
        r = [0, 3, 2, 9] # and denominator 14 to scale back from fractions
        d = 14
        b = AmcTest.calculate_b(m)
        b0 = b[0]
        self.assertTrue(amc.format_result(b0) == [0, 3, 2, 9, 14])

        # TEST 2
        m = [[1,1,1,1], #s0
             [0,0,0,0], #s1
             [0,0,0,0], #s2
             [1,2,3,4]] #s3
        r = [8, 9] # and denominator 17 to scale back from fractions
        d = 17 # denominator to scale back to integers after normalization
        b = AmcTest.calculate_b(m)
        b0 = b[0] # to test transitions only from s0
        bd = [round(i*d) for i in b0]
        self.assertTrue(amc.format_result(b0) == [8, 9, 17])

    def test_b(self):
        # TEST 1
        m = [[0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
             [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
             [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
             [0,0,0,0,0,0],  # s3 is terminal
             [0,0,0,0,0,0],  # s4 is terminal
             [0,0,0,0,0,0]]
        r = [0, 3, 2, 9] # and denominator 14 to scale back from fractions
        d = 14
        b = AmcTest.calculate_b(m)
        lcm = amc.compute_lcm(b[0])
        b0 = b[0]
        bd = [round(i*d) for i in b0]
        self.assertTrue(lcm == d)
        self.assertTrue(bd == r)

        # TEST 2
        # test 2
        m = [[1,1,1,1], #s0
             [0,0,0,0], #s1
             [0,0,0,0], #s2
             [1,2,3,4]] #s3
        r = [8, 9] # and denominator 17 to scale back from fractions
        d = 17 # denominator to scale back to integers after normalization
        b = AmcTest.calculate_b(m)
        lcm = amc.compute_lcm(b[0])
        b0 = b[0] # to test transitions only from s0
        bd = [round(i*d) for i in b0]
        self.assertTrue(lcm == d)
        self.assertTrue(bd == r)

    def test_zero_terminal(self):
        m = [[0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [0, 0, 0, 0, 0]
             ]
        b = AmcTest.calculate_b(m)
        self.assertTrue(b == [1,0,0,1])

        m = [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [0, 0, 0, 0, 0]
             ]
        b = AmcTest.calculate_b(m)
        self.assertTrue(b == [1,0,0,0,1])

    def test_more(self):
        # TEST 1
        m = [[0, 2, 1, 0, 0],
             [0, 0, 0, 3, 4],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]
             ]
        self.assertEqual([Fraction(7,21), Fraction(6,21), Fraction(8,21)], AmcTest.markov_probabilities(m))

        # TEST 2
        m = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0]]
        self.assertEqual([0, Fraction(3,14), Fraction(2,14), Fraction(9,14)], AmcTest.markov_probabilities(m))

        # TEST 3
        m = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.assertEqual([Fraction(1,5), Fraction(1,5), Fraction(1,5), Fraction(1,5), Fraction(1,5)], AmcTest.markov_probabilities(m))

        # TEST 4
        probs = AmcTest.markov_probabilities([
            [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.assertTrue(sum(probs) == 1)
        self.assertEqual([Fraction(1,3),
                          Fraction(1,6),
                          Fraction(1,6),
                          Fraction(1,6),
                          Fraction(1, 6)],
                          probs)
        # TEST 5
        probs = AmcTest.markov_probabilities([
            [0, 86, 61, 189, 0, 18, 12, 33, 66, 39],
            [0, 0, 2, 0, 0, 1, 0, 0, 0, 0],
            [15, 187, 0, 0, 18, 23, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        )
        self.assertTrue(sum(probs) == 1)
        self.assertEqual([Fraction(6,100),
                          Fraction(44,100),
                          Fraction(4,100),
                          Fraction(11,100),
                          Fraction(22,100),
                          Fraction(13, 100)],
                          probs)
        # TEST 6
        probs = AmcTest.markov_probabilities([
            [0, 0, 0, 0, 3, 5, 0, 0, 0, 2],
            [0, 0, 4, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 4, 4, 0, 0, 0, 1, 1],
            [13, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 1, 8, 7, 0, 0, 0, 1, 3, 0],
            [1, 7, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.assertTrue(sum(probs) == 1)
        self.assertEqual([Fraction(1,5),
                          Fraction(1,5),
                          Fraction(1,5),
                          Fraction(2, 5)],
                          probs)

        probs = AmcTest.markov_probabilities([
            [1, 1, 1, 1, 1,],
            [0, 0, 0, 0, 0,],
            [1, 1, 1, 1, 1,],
            [0, 0, 0, 0, 0,],
            [1, 1, 1, 1, 1,]
            ])

if __name__ == "__main__":
    unittest.main()
