from PIL import ImageFont
from flask import Flask, jsonify, request
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from apscheduler.schedulers.background import BackgroundScheduler
from configparser import ConfigParser
import time
from datetime import datetime

from camera import Camera
from tgbot import TGBot
from tool import draw_date_text
from storage import Storage 
from workerskv import WorkersKV

app = Flask(__name__)

@app.route('/status/', methods=['GET'])
def status():
	return jsonify({"ok": True})

#  nohup python3 -u app.py > out.log 2>&1 &
@app.route('/flower-photo/', methods=['POST'])
def flower_photo():
	if request.headers.get('Authorization').split()[1] == auth_bearer_token:
		content = request.json
		chat_id = content["chat_id"] 
		command = content["command"]
		
		now = datetime.now()
		filename = now.strftime("%Y%m/%d/%H_%M") + '.jpg'

		global last_filename

		# cache within-1-minute photo
		if (now.strftime("%Y%m/%d/%H_%M") + '.jpg') == last_filename:
			res = my_TGBot.send_storage_photo(last_filename, chat_id)
		else:
			pil_image = my_cam.capture()
			pil_image = draw_date_text(pil_image, font)
			res = my_TGBot.send_photo(pil_image, chat_id)
			last_filename = my_storage.upload_image(pil_image)
			#my_workerskv.put(last_filename, last_filename, str(round(time.time()) + 120))

		if res:
			return jsonify({"ok": True})
		else:
			return jsonify({"error": "Fail to send message."}), 500

	else:
		return jsonify({"error": "Unauthorized Request"}), 401

def capture_worker():
	now = datetime.now()
	hour_str = now.strftime("%H")

	if hour_str not in ['23', '00', '01', '02', '03', '04', '05', '06']:
		print('Schedule work started at time' + hour_str)
		global last_filename
		pil_image = my_cam.capture()
		pil_image = draw_date_text(pil_image, font)
		last_filename = my_storage.upload_image(pil_image)

if __name__ == '__main__':
	cfg = ConfigParser()
	cfg.read('conf/config.ini')
	auth_bearer_token = cfg.get('AUTH', 'BEARER_TOKEN')

	font = ImageFont.truetype('fonts/FreeMonoBold.ttf', 80)
	last_filename = 'na'

	my_cam = Camera()
	my_TGBot = TGBot(cfg.get('TG_BOT', 'TOKEN'), cfg.get('CF_R2_STORAGE', 'BUCKET_ID'))
	my_storage = Storage(cfg.get('CF_R2_STORAGE', 'CF_ID'), cfg.get('CF_R2_STORAGE', 'KEY_ID'), cfg.get('CF_R2_STORAGE', 'SECRET_KEY'))
	#my_workerskv = WorkersKV(cfg.get('CF_KV', 'CF_ACCOUNT'), cfg.get('CF_KV', 'CF_TOKEN'), cfg.get('CF_KV', 'KV_NS_ID'))

	sched = BackgroundScheduler(daemon=True, timezone="Asia/Singapore")
	sched.add_job(capture_worker, 'interval', minutes=60)
	sched.start()
	
	CORS(app, resources=r'/*')

	http_server = WSGIServer((cfg.get('HTTP_SERVER', 'HOST'), cfg.getint('HTTP_SERVER', 'PORT')), app)

	print('Web server started.')
	http_server.serve_forever() 
