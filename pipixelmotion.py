#!/usr/bin/python

# Copyright 2014 Clayton Lambert
# https://github.com/claytonn
# http://claytonn.com

# **Note: This per pixel method is really really inefficient. Seriously. 

import io
import picamera
from PIL import Image
scan = True
images = []


color_offset = 25 # Adjusts for slight varitaions in color

while(scan):
	stream = io.BytesIO()
	with picamera.PiCamera() as camera:
		camera.resolution = (64,36) #Low Res For Faster Comparisons
		camera.start_preview()
		camera.capture(stream, format='jpeg')
	stream.seek(0)	

	if(len(images)!=2):
		images.append(Image.open(stream))
	else:
		images[0] = Image.open(stream)
	
	x = 0
	y = 0
	diff = 0

	if len(images) != 1:
		#Start On X and Move Down Y 
		while(x < images[0].size[0]):
			while(y < images[0].size[1]):

				#Add Up All RGB Values For Current Pixel
				img1 = images[1].getpixel((x,y))
				val = img1[0] + img1[1] + img1[2]
				img2 = images[0].getpixel((x,y))
				val2 = img2[0] + img2[1] + img2[2]
				
				pd = abs(val2-val)
				
				if(pd > color_offset):
					diff += 1
				y += 1
				
			#Move Right 1 & Reset Y For Next Loop
			x+=1
			y=0
		
		changed  = (diff * 100) / (images[0].size[0] * images[0].size[1])
		print str(changed) + "% changed."
		images[1] = images[0]
