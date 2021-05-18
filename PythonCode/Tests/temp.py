from fastapi.testclient import TestClient
from PythonCode.GUI.GUIAdapter import gui_adapter


if __name__ == '__main__':

    client = TestClient(gui_adapter)
    response = client.get("/search/", json={"filename": "NONE"})
    print(response)
    print(response.status_code)
    print(response.json())
    # self.assertEqual(response.status_code, 200)
    # self.assertEqual(response, False)