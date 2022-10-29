import requests
from io import BytesIO

class TGBot:
    def __init__(self, token):
        self.tg_endpoint = "https://api.telegram.org/bot" + token

    def send_photo(self, image, chat_id, caption=''):
        image_buf = BytesIO()
        image.save(image_buf, format='JPEG')
        image_buf.seek(0)

        tg_sp_endpoint = self.tg_endpoint + "/sendPhoto"
        data = {'chat_id': chat_id, 'caption': caption}
        
        res =  requests.post(url = tg_sp_endpoint, data = data, files = {'photo': image_buf})

        if res.ok:
            return True
        else:
            return False
        
    def send_message(self, text, chat_id):
        tg_sm_endpoint = self.tg_endpoint + "/sendMessage"
        data = {'chat_id': chat_id, "text": text, "parse_mode": "HTML"}
        
        res =  requests.post(url = tg_sm_endpoint, data = data)

        if res.ok:
            return True
        else:
            return False
