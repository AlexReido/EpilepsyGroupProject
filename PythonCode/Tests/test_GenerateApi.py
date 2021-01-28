import unittest
from multiprocessing import Process
# from .. import GenerateModel
import uvicorn
import requests
import time
import bct


class TestGenerate(unittest.TestCase):
    def setUp(self):
        self.proc = Process(target=uvicorn.run,
                            args=('PythonCode.GenerateModel:app',),
                            kwargs={
                                "host": "127.0.0.1",
                                "port": 5000,
                                "log_level": "info"},
                            daemon=True)
        self.proc.start()
        time.sleep(8)

    def tearDown(self):
        self.proc.terminate()

    def test_ArtificialRandom(self):
        response = requests.get('http://127.0.0.1:5000/model/artificial/',
                                params={'nodes': 30, 'edges': 200, 'structure': 'random'})
        self.assertEqual(response.status_code, 200)
        print(response)
        print(response.headers['content-type'])
        net = response.json()
        print(type(net))
        print(net)
        self.assertEqual(len(net), 30)

    def test_ArtificialLattice(self):
        response = requests.get('http://127.0.0.1:5000/model/artificial/',
                                params={'nodes': 30, 'edges': 200, 'structure': 'lattice'})
        self.assertEqual(response.status_code, 200)
        print(response)
        print(response.headers['content-type'])
        net = response.json()
        print(type(net))
        print(net)
        self.assertEqual(len(net), 30)
        print(bct.assortativity_wei(net))

    def test_ArtificialToeplitz(self):
        response = requests.get('http://127.0.0.1:5000/model/artificial/',
                                params={'nodes': 30, 'edges': 200, 'structure': 'toeplitz'})
        self.assertEqual(200, response.status_code) # (Expected, actual)
        print(response)
        print(response.headers['content-type'])
        net = response.json()
        print(type(net))
        print(net)
        self.assertEqual(30, len(net))


if __name__ == '__main__':
    unittest.main()
