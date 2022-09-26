# python detect_mask_video.py ile program başlatılır.
from array import array
#from curses import window
from importlib.resources import path
from sqlite3 import Row
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import time as t
import tkinter as tk  # python 3
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import sys
from tkinter import *
import glob

def detect_and_predict_mask(frame, faceNet, maskNet):
	# çerçeve boyutları belirlenir ve bir blob alınır
	# Blob, bir görüntü içindeki tonlama değeri gibi bazı ortak özellikleri paylaşan
	# birbirine bağlı pikseller topluluğudur. OpenCV blobları tespit etmek ve onları 
	# farklı özelliklerine göre filtrelemek için hazır bir fonksiyon (SimpleBlobDetector) sunar.
	(h, w) = frame.shape[:2] 
	blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
		(104.0, 177.0, 123.0))
	

	# blobu ağ üzerinden geçirir ve yüz algılamalarını alır 
	faceNet.setInput(blob)
	detections = faceNet.forward()

	# yüz listesini, bunların karşılık gelen konumlarını başlat,
	# face mask ağımızdan tahminlerin listesi
	faces = []
	locs = []
	preds = []

	# loop da tespit
	for i in range(0, detections.shape[2]):
		#
		# tespit
		confidence = detections[0, 0, i, 2]

		# zayıf algılanan tespitler filtreleniyor
		# güç olarak algılanan minimum tespitten büyük olanları al 
		if confidence > args["confidence"]:
			# sınırlayıvıyı kutunun x,y koordinatlarını hesaplayan nesne
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			
			
			

			# sınırlayıcı kutuların boyutları dahilinde olduğundan emin olun
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# yüz ROI'sini çıkarır, BGR'den RGB  dönüştürür ?????????
			# 224x224'e  boyutlandırır
			face = frame[startY:endY, startX:endX]
			if face.any():
				face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
				face = cv2.resize(face, (224, 224))
				face = img_to_array(face)
				face = preprocess_input(face)
				
				# yüz ve sınırlayıcı kutuları kendi kutularına eklenir
				# listeler
				faces.append(face)
				locs.append((startX, startY, endX, endY))

	# en az bir yüz algılandıysa tahminde bulunur
	if len(faces) > 0:

		# yukarıdaki for döngüsünde,
		# daha hızlı çıkarım için *tümü* üzerinde toplu tahminler yapılacaktır,
		# aynı anda birden fazla yüz tahmininde bulunabilir :))
		
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	# yüz konumlarının 2 demetini ve bunlara karşılık gelenleri döndürür
	# konum
	return (locs, preds)

# argüman ayrıştırıcısını oluşturulur ve argümanları ayrıştırılır
# yani face ve mask detector modelleri ile ayrıştırır
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,
	default="face_detector",
	help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
	default="mask_detector.model",
	help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# face detector modeli diskten yüklenir
print("[BILGI] yuz okuma dedektoru yukleniyor...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# face mask detector modeli diskten yüklenir
print("[BILGI] maske okuma dedektoru yukleniyor...")
maskNet = load_model(args["model"])

# kamera başlatma
print("[BILGI] kamera baslatiliyor...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# video akışından kareler üzerinde döngü
while True:
	# akıtılan video akışından çerçeveyi alır ve 
	# maksimum 400 piksel genişliğe sahip olacak şekilde yeniden boyutlandırır
	frame = vs.read()
	frame = imutils.resize(frame, width=400 )
	
	# çerçevedeki yüzleri algılanır ve yüzlerde masske takıp takmadıklarını belirlenir
	(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

	# algılanan yüz konumları ve karşılık gelenleri döngüye alır
	for (box, pred) in zip(locs, preds):
		# sınırlayıcı kutuyu ve tahminleri açar, tahminler %100 üzerinden değerlendirilir
		(startX, startY, endX, endY) = box
		(mask, withoutMask) = pred

		# başlatılan video çerçevesi, sınırlayıcı kutu ve metin
		# için kullanılacak sınıf etiketi ve rengi belirlendi -> yeşil ve kırmızı
		label = "Maske var" if mask > withoutMask else "Maske yok"
		color = (0, 255, 0) if label == "Maske var" else (0, 0, 255)
			
		# yüzde tahminini ekler label da
		label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

		# çıktıda label i ve sınırlayıcı kutuyu göster
		cv2.putText(frame, label, (startX, startY - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

		timestr = t.strftime("%Y%m%d-%H%M%S")

	
	#çıktı çerçevesini göster
	cv2.imshow("Maske Kontrolu", frame)
	key = cv2.waitKey(1) & 0xFF

	crop_frame = frame[startY:endY, startX:endX] #box ın koordinatları kadar kes

	# img yakala kaydet 

	if mask>withoutMask :
		img_1 = cv2.imwrite("maskeli/maskeli%s.jpg" % timestr, crop_frame)
		#cv2.imshow("maskeli", crop_frame)
	else :
		img = cv2.imwrite("maskesiz/maskesiz%s.jpg" % timestr, crop_frame)
		#cv2.imshow("maskesiz", crop_frame)


	#kaydedilen fotograflar array e atıldı
	maskesiz_images = np.array([cv2.imread(file) for file in glob.glob("maskesiz/*.jpg")])
	maskeli_images = np.array([cv2.imread(file) for file in glob.glob("maskeli/*.jpg")])

	num_of_first =maskesiz_images.shape[0] #arrayin ilk elemanı
	num_of_second = maskeli_images.shape[0]

	#image_array = np.concatenate((first_images,second_images),axis=0) #tek array yapmak için

#######################################
	# i = 0
	# while i < num_of_first:
	# # image = cv2.imread ("C:/Users/aysegul/Desktop/aau/maskesiz/*jpg")
	# #maskesiz_images.append (image)
	# #print('image_array shape:', np.array(maskesiz_images).shape)
	# 	gor1= cv2.imshow('MASKESİZ', maskesiz_images[i]) #FOTOLARI GÖRÜNTÜLÜYOR 
	# 	i = i + 1
	# # # 	#cv2.waitKey(5)
		
	# while i < num_of_second:
	# 	gor2= cv2.imshow('MASKELİ', maskeli_images[i])
	# 	i = i + 1
######################################################

		# 'q' tuşuna basılmışsa, döngüden çıkılır
	if key == ord("q"):
		break



# durdurma
cv2.destroyAllWindows()
vs.stop()


















