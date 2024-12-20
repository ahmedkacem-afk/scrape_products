import requests


class SendRequest :
    
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers

    def send_request(self):
        response = requests.get(self.url , headers = self.headers)
        return response
    
SendRequest("https://auto-pieces.tn/index.php?controller=search&s=embrayage").send_request()