import unittest
from multiprocessing import Process
# from .. import GenerateModel
import asyncio
import uvicorn
import requests
import time


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
        time.sleep(4)

    def tearDown(self):
        self.proc.terminate()

    def test_ArtificialApi(self):
        response = requests.get('http://127.0.0.1:5000/model/artificial/',
                                params={'nodes': 30, 'edges': 200, 'structure': 'random'})
        self.assertEqual(response.status_code, 200)
        print(response)
        print(response.headers['content-type'])
        net = response.json()
        print(type(net))
        print(net)
        self.assertEqual(len(net), 30)


if __name__ == '__main__':
    unittest.main()
