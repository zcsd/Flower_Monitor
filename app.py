from PIL import ImageFont
from flask import Flask, jsonify, request
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from configparser import ConfigParser
import time
from datetime import datetime

from camera import Camera
from tgbot import TGBot
from tool import draw_date_text, draw_env_text
from storage import Storage 
from workerskv import WorkersKV
from serial_comm import SerialComm
from database import Database

app = Flask(__name__)

@app.route('/status/', methods=['GET'])
def status():
	return jsonify({"ok": True})

@app.route('/flower-env/', methods=['POST'])
def flower_env():
	if request.headers.get('Authorization').split()[1] == auth_bearer_token:
		print("-------------------------------------------------------------")
		print("[✔] Authorized Request in flower-env.", datetime.now())
		content = request.json

		now = datetime.now()

		temperature, humidity = my_serial.get_temperature_humidity()
		lux = my_serial.get_illuminance()
		
		values = ['NA', temperature, humidity, lux]
		my_db.insert_env_data(now, values)

		return jsonify({"ok": True})
	else:
		print("-------------------------------------------------------------")
		print("[✗] Unauthorized Request in flower-env.", datetime.now())
		return jsonify({"error": "Unauthorized Request"}), 401

#  nohup python3 -u app.py > out.log 2>&1 &
@app.route('/flower-status/', methods=['POST'])
def flower_status():
	if request.headers.get('Authorization').split()[1] == auth_bearer_token:
		print("-------------------------------------------------------------")
		print("[✔] Authorized Request in flower-status.", datetime.now())
		content = request.json
		chat_id = content["chat_id"] 
		send_to_chat = content["with_chat"]
		is_cron = content["is_cron"] 
		
		now = datetime.now()
		filename = now.strftime("%Y%m/%d/%H_%M") + '.jpg'

		global last_filename

		if (now.strftime("%Y%m/%d/%H_%M") + '.jpg') == last_filename:
			# use cache within-1-minute photo
			res = my_TGBot.send_storage_photo(last_filename, chat_id)
		else:
			temperature, humidity = my_serial.get_temperature_humidity()
			lux = my_serial.get_illuminance()

			pil_image = my_cam.capture()
			pil_image = draw_date_text(pil_image, font)
			pil_image = draw_env_text(pil_image, font, [temperature, humidity, lux])

			if send_to_chat:
				res = my_TGBot.send_photo(pil_image, chat_id)
				if is_cron:
					print("Cron Job and sent to TG group.", datetime.now())
				else:
					print("Command Job and sent to TG group.", datetime.now())
			else:
				print("Cron Job and NOT send to TG group.", datetime.now())
				res = True
			
			last_filename = my_storage.upload_image(pil_image)
			values = [last_filename, temperature, humidity, lux]
			my_db.insert_env_data(now, values)
			#my_workerskv.put(last_filename, last_filename, str(round(time.time()) + 120))

		if res:
			return jsonify({"ok": True})
		else:
			return jsonify({"error": "Fail to send message."}), 500

	else:
		print("-------------------------------------------------------------")
		print("[✗] Unauthorized Request in flower-status.", datetime.now())
		return jsonify({"error": "Unauthorized Request"}), 401

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
	my_serial = SerialComm()
	my_db = Database(cfg.get('DB', 'HOST'), cfg.get('DB', 'DATABASE'), cfg.get('DB', 'USER'), cfg.get('DB', 'PASSWORD'))
	
	CORS(app, resources=r'/*')

	http_server = WSGIServer((cfg.get('HTTP_SERVER', 'HOST'), cfg.getint('HTTP_SERVER', 'PORT')), app)

	print('Web server started.', datetime.now())
	http_server.serve_forever() 
