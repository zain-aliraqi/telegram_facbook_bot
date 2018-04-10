#  by zain aliraqi
from flask import Flask, request, render_template,send_file
import requests

app = Flask(__name__)

id_t=""

f_token = "facebook_token"
VERIFY_TOKEN = "zain_iq"

token='telegram_token'

#------id------------------
fb_id = 'facebook id for your acound'
tele_id = 4**** #telegram id 
#______msg_Error_____________

@app.route('/')
def index():
	return '<h1>is work!</h1>'



#---------------------- faceBook -----------------------
#   download_img_facebook
def d_img_f(type_f_t,url_f):
	r = requests.get(url_f)
	if r.status_code == 200:
		send_photo_tele(tele_id,r.content)
		pass
		# with open("sample1.{}".format(type_f_t), 'wb') as f:
		# 	f.write(r.content)

#send img from tele to face
def send_photo_f(user_id,img):
	data_ph = {
	  "recipient":{"id":"1*******"},
		"message":{
			"attachment":{
				"type":"image", 
				"payload":{
					"url":'https://www.google.iq/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png', 
					"is_reusable":True
	      }
	    }
	  }
}

	requests.post("https://graph.facebook.com/v2.6/me/messages?access_token={}".format(f_token), json=data_ph)
	


# send message to facebook
def send_m_f(user_id,msg):
	data = {
		"recipient": {"id": user_id},
		"message": {"text": msg}
	}
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + f_token, json=data)

#-------- flask ---- face ---------------------
@app.route('/faceBot', methods=['GET'])
def handle_verification():
	if request.args['hub.verify_token'] == VERIFY_TOKEN:
		return request.args['hub.challenge']
	else:
		return "Invalid verification token"

@app.route('/faceBot', methods=['POST'])
def faceBot():
	global id_t 
	data = request.get_json()
	if 'entry' in data:
		if 'messaging' in data['entry'][0]:
			sender_id = data['entry'][0]['messaging'][0]['sender']['id']
			if sender_id == fb_id:
				if 'message' in data['entry'][0]['messaging'][0]:
					if 'attachments' in data['entry'][0]['messaging'][0]['message']:
						if 'payload' in data['entry'][0]['messaging'][0]['message']['attachments'][0]:
							if 'url' in data['entry'][0]['messaging'][0]['message']['attachments'][0]['payload']:
								type_f = data['entry'][0]['messaging'][0]['message']['attachments'][0]['type']
								url_f = data['entry'][0]['messaging'][0]['message']['attachments'][0]['payload']['url']
								type_f_t = url_f.split('?')[0].split('.')[-1]
								#---------?
								
								if type_f == 'image':
									d_img_f(type_f_t,url_f)

					elif 'text' in data['entry'][0]['messaging'][0]['message']:
						text = data['entry'][0]['messaging'][0]['message']['text'].encode('utf-8')
						if text.split('#/#')[0] == '$':
							id_t = text.split('#/#')[1]
							send_m_f(fb_id, 'Done add id: ' + id_t)
						elif len(text.split('#/#')) >1:
							if text.split('#/#')[0].isdigit():
								id_t=text.split('#/#')[0]
								text=text.split('#/#')[1]
								send_m_tele(id_t,text)
							else:
								send_m_f(fb_id, 'pelse entrt [id #/# msg] !')
						elif id_t != '':
							send_m_tele(id_t,text)
						else:
							send_m_f(fb_id, 'pelse entrt [id #/# user] !')
							

							
					



	else:
		pass


								
			
	# print '\n\n========== all dara facebook ==================\n\n'
	# print data
	# print '\n\n==============----===========================\n\n'
	return "<center><h1>Facebook Bot <p>by Aliraqi</p></h1></center>",200

# -------Telegram -------
def get_file_id(file_id):
	url_file_id = "https://api.telegram.org/bot{}/getFile?file_id={}".format(token,file_id)
	resp = requests.post(url_file_id)
	json_f = resp.json()
	if json_f['ok']:
		file = json_f['result']['file_path']
		url_file = "https://api.telegram.org/file/bot{}/{}".format(token,file)
		send_photo_f(fb_id,url_file)
		# resp_file = requests.get(url_file)
		# if resp_file.status_code == 200:
		# 	send_photo_f(fb_id,resp_file.content)
			# with open("photo.jpg", 'wb') as f:
			# 	f.write(resp_file.content)
		
def send_m_tele(chat_id,message):
	resp = requests.post('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(token, chat_id, message))
	resp.content
def send_photo_tele(chat_id,img):
	img = {'photo':img}
	resp = requests.post('https://api.telegram.org/bot{}/sendPhoto?chat_id={}'.format(token, chat_id),files=img)
	resp.content
#--------flask---------
@app.route('/teleBot', methods=['POST'])
def teleBot():
	# if request.method == 'POST':
	update = request.get_json()

	if "message" in update:
		chat_id = update['message']['chat']['id']
		first_name = update['message']['chat']['first_name']
		tag_inf = "ID: {} \nName: {} \n".format(chat_id,first_name)

		if 'photo' in update['message']:
			photo_id = update['message']['photo'][2]['file_id']
			if 'caption'in update['message'] :
				caption = update['message']['caption'].encode('utf-8')
				send_m_f(fb_id, tag_inf+str(caption))
			send_m_f(fb_id, tag_inf)	
			get_file_id(photo_id)

		elif 'sticker' in update['message']:
			sticker = update['message']['sticker']['file_id']
			get_file_id(sticker)
			# photo(chat_id)

		elif 'text' in update['message']:
			text = update["message"]["text"].encode('utf-8')
			send_m_f(fb_id, tag_inf+str(text))

		elif 'voice' in update['message']:
			voice = update['message']['voice']['file_id']
			if 'caption'in update['message'] :
				caption = update['message']['caption'].encode('utf-8')
				send_m_f(fb_id, tag_inf+str(caption))

		elif 'video' in update['message']:
			voice = update['message']['video']['file_id']
			if 'caption'in update['message'] :
				caption = update['message']['caption'].encode('utf-8')
				send_m_f(fb_id, tag_inf+str(caption))	
	# print '------------tele data -----------'
	# print update
	# print '------------tele data -----------'
	return "<center><h1>Telegram Bot <p>by Aliraqi</p></h1></center>", 200



if __name__ == '__main__':
	app.run(debug=False)#True||False
