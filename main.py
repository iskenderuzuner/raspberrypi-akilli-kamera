import cv2
import sys
from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading

email_update_interval = 600 # bu zaman araliginda yalnizca bir kez e-posta gonderir
video_camera = VideoCamera(flip=True) # Dikey olarak bir kamera nesnesi olusturur
object_classifier = cv2.CascadeClassifier("models/fullbody_recognition_model.xml") # OpenCV Siniflandiricisi

# Kullanici adi sifre bilgileri admin panel
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'iskender'
app.config['BASIC_AUTH_PASSWORD'] = '42520312031'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0

def check_for_objects():
	global last_epoch
	while True:
		try:
			frame, found_obj = video_camera.get_object(object_classifier)
			if found_obj and (time.time() - last_epoch) > email_update_interval:
				last_epoch = time.time()
				print "Mail Gonderiliyor..."
				sendEmail(frame)
				print "done!"
		except:
			print "E-posta gonderilirken hata olustu: ", sys.exc_info()[0]

@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
