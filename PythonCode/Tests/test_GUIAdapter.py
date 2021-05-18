import unittest
from fastapi.testclient import TestClient
from PythonCode.GUI.GUIAdapter import gui_adapter


# TODO use Test client from https://fastapi.tiangolo.com/tutorial/testing/
class TestGenerate(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(gui_adapter)

    def tearDown(self):
        pass

    def test_ArtificialNetworkdefaultNet(self):
        response = self.client.get('/')  #: 30, 'edges': 200, 'structure': 'lattice'})
        self.assertEqual(response.status_code, 200)
        net = response.json()
        print(len(net))
        self.assertEqual(len(net), 29343)

    def test_ArtificialNetworkrandomNet(self):
        response = self.client.get('/?artificial=True&nodes=30')  #: 30, 'edges': 200, 'structure': 'lattice'})
        self.assertEqual(response.status_code, 200)
        net = response.json()
        # print(l)
        self.assertLessEqual(len(net), 21000)

    def test_searchStatus(self):
        response = self.client.get("/search/", json={"filename": "NOFILE"})
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response, False)

    # def test_ArtificialToeplitz(self):
    #     response = requests.get('http://127.0.0.1:5000/model/artificial/',
    #                             params={'nodes': 30, 'edges': 200, 'structure': 'toeplitz'})
    #     self.assertEqual(200, response.status_code) # (Expected, actual)
    #     print(response)
    #     print(response.headers['content-type'])
    #     net = response.json()
    #     print(type(net))
    #     print(net)
    #     self.assertEqual(30, len(net))


if __name__ == '__main__':
    client = TestClient(gui_adapter)
    response = client.get(
        '/model/artificial/?artificial=False&nodes=30')  #: 30, 'edges': 200, 'structure': 'lattice'})
    assert (response.status_code == 200)
    print(response)
    # unittest.main()
