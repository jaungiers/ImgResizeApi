import os
import time
import numpy as np
import cv2
import urllib2
from flask import Flask, render_template, request

ImgResizeApi = Flask(__name__)

@ImgResizeApi.route('/')
def main():
	return render_template('index.html')

@ImgResizeApi.route('/api')
def imgRs():
	imgUrl = request.args.get('iurl')
	width  = request.args.get('w')
	height = request.args.get('h')
	inpImg = fetchImg(imgUrl)
	outImg = cv2.resize(inpImg, (int(width), int(height)))

	filename = 'tempImg.png'
	cv2.imwrite('static/' + filename, outImg)
	return render_template('index.html', filename=filename, noCache=time.time())

def fetchImg(imgUrl):
	req = urllib2.urlopen(imgUrl)
	arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
	img = cv2.imdecode(arr,-1)
	return img

if __name__ == '__main__':
	ImgResizeApi.run()