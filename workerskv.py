import requests

BASE_URL = "https://api.cloudflare.com/client/v4"
HEADERS = {"Content-Type": "application/json"}

class WorkersKV():
    def __init__(self, cf_account, cf_token, namespace):
        self.token = cf_token
        self.headers = HEADERS
        self.headers["Authorization"] = "Bearer " + self.token
        self.base_url = (
            BASE_URL + "/accounts/" + cf_account + "/storage/kv/namespaces/" + namespace
        )

    def list_keys(self):
        response = requests.get(
            self.base_url + "/keys",
            headers=self.headers
        )
        return response
    
    def get(self, key):
        response = requests.get(
            self.base_url + "/values/" + key,
            headers=self.headers
        )
        return response
    
    def put(self, key, value, expiration):
        response = requests.put(
            self.base_url + "/values/" + key + '?expiration=' + expiration,
            headers=self.headers,
            data=value
        )
        if response.status_code == 200:
            print(key + ' wrote to KV successfully.')
        else:
            print(key + ' failed to write to KV.')
        
        return response

    def delete(self, key):
        response = requests.delete(
            self.base_url + "/values/" + key,
            headers=self.headers
        )
        return response