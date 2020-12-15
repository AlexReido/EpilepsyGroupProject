import unittest
import PythonCode.GenerateModel as gm
import numpy as np


class TestArtificailNetwork(unittest.TestCase):
    def test_nodesandConnections(self):
        k = 30
        m = 100
        # structural network
        sn = gm.getStructuralnetwork(k,m)
        self.assertEqual(len(sn), 30)
        self.assertEqual(np.count_nonzero(sn == 1), 100)

if __name__ == '__main__':
    unittest.main()
