import os
from flask import Flask, render_template, request, send_file

import time, datetime
import random
import numpy as np
import cv2
import urllib2

ImgResizeApi = Flask(__name__)

@ImgResizeApi.route('/')
def main():
	cleanup_temps()
	return render_template('index.html')

@ImgResizeApi.route('/api')
def imgRs():
	basePath = 'static/images/temp/'
	imgUrl = request.args.get('iurl')
	width  = request.args.get('w')
	height = request.args.get('h')
	inpImg = fetchImg(imgUrl)
	outImg = cv2.resize(inpImg, (int(width), int(height)))
	'''
	filename = str(time.time()) +  str(random.randrange(0,100000)) + '.png'
	cv2.imwrite(basePath + filename, outImg)
	return send_file(basePath + filename, mimetype='image/png')
	'''
	return render_template('index.html')

def fetchImg(imgUrl):
	req = urllib2.urlopen(imgUrl)
	arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
	img = cv2.imdecode(arr,-1)
	return img

def cleanup_temps():
	basePath = 'static/images/temp/'
	deleteDelay = 20
	for f in os.listdir(basePath):
		if os.path.getctime(basePath + f) < (time.time() - deleteDelay):
			os.remove(basePath + f)

if __name__ == '__main__':
	ImgResizeApi.run()