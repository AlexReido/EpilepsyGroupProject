import unittest
import PythonCode.GenerateNetsMarc as GnM


def find_average_degree(net):
    total_edges = 0
    total_nodes = len(net)
    for i in range(len(net)):
        for j in range(len(net[0])):
            if net[i, j] == 1:
                total_edges += 1
    return int(round(total_edges / total_nodes))


class TestGenerateNetsMarc(unittest.TestCase):

    def test_sf_und(self):
        n = 40
        k = 5
        gamma = 3
        net = GnM.sf_und(n, k, gamma)

        # Check size of network
        self.assertEqual(len(net), n)
        self.assertEqual(len(net), len(net[0]))

        # Check degree of network
        average_degree = find_average_degree(net)
        self.assertEqual(average_degree, k*2)


if __name__ == '__main__':
    unittest.main()
