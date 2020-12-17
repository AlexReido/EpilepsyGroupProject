import unittest
import PythonCode.GenerateModel as gm
import numpy as np
# import test_Gener

class TestArtificialNetwork(unittest.TestCase):
    def test_nodesandConnections(self):
        k = 30
        m = 100
        # structural network
        sn = gm.getStructuralnetwork(k,m, "random")
        self.assertEqual(len(sn), k)
        self.assertEqual(np.count_nonzero(sn == 1), m)

if __name__ == '__main__':
    unittest.main()
