import webview

if __name__ == '__main__':
    webview.create_window('Hello world', 'http://127.0.0.1:1337/')
    webview.start()