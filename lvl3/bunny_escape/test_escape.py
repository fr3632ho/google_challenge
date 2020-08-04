# TESTS
import escape as esc, unittest, escape2 as esc2
from copy import deepcopy

class TestEsc(unittest.TestCase):

    @staticmethod
    def bfs(m):
        return esc2.solution(m)

    @staticmethod
    def bell_ford(m):
        return esc.solution(m)

    @staticmethod
    def algs(m):
        return TestEsc.bell_ford(m), TestEsc.bfs(m)

    def test_examples(self):
        # Test one
        m = [[0, 1, 1, 0],
              [0, 0, 0, 1],
              [1, 1, 0, 0],
              [1, 1, 1, 0]]
        bell, bfs = TestEsc.algs(m)
        self.assertTrue(bell == bfs == 7)

        # Test two
        m = [[0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1],
              [0, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0]]
        bell, bfs = TestEsc.algs(m)
        self.assertTrue(bell == bfs == 11)

        # Test three
        m = [[0, 1],
             [1, 0]]
        bell, bfs = TestEsc.algs(m)
        self.assertTrue(bell == bfs == 3)

        # Test four
        m = [[0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0]]
        bell, bfs = TestEsc.algs(m)
        self.assertTrue(bell == bfs == 10)


    def test_edgecases(self):
        # Simple 3x3
        m = [[0, 0, 1],
             [0, 0, 1],
             [1, 1, 0]]
        bell, bfs = TestEsc.algs(m)
        self.assertTrue(bell == bfs == 5)

        # Max width and minimal height
        m = [[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0]]

        bell, bfs = TestEsc.algs(m)
        self.assertTrue(bell == bfs == 21)

        # Max width and minimal height
        m = [[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,0]]

        bell, bfs = TestEsc.algs(m)
        self.assertTrue(bell == bfs == 21)

        # Max height and minimal width
        m = [[0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,0]]
        bell, bfs = TestEsc.algs(m)
        self.assertTrue(bell == bfs == 21)

        # Max height and minimal width
        m = [[0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [0,1],
             [1,0]]
        bell, bfs = TestEsc.algs(m)
        self.assertTrue(bell == bfs == 21)

    def test_larger(self):
        m =  [[0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 1],
              [0, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 0],
              [0, 0, 0, 1, 1, 0]]
        bell, bfs = TestEsc.algs(m)
        self.assertTrue(bell == bfs == 11)

        ##
        m = [[0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0],
             [1,1,1,1,1,1,1,1,1,1,1,1,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0]]
        bell, bfs = TestEsc.algs(m)
        self.assertTrue(bell == bfs == 22)

        ##
        m = [[0, 1, 0, 0, 0],
             [0, 0, 0, 1, 0],
             [0, 0, 1, 1, 1],
             [0, 1, 1, 0, 0],
             [0, 1, 1, 0, 0]]
        bell, bfs = TestEsc.algs(m)
        self.assertTrue(bell == bfs == 11)



if __name__ == "__main__":
    unittest.main()
