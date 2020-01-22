import numpy as np
import cv2
#import os
import dlib
from PIL import Image



recognizer = cv2.createFisherFaceRecognizer()

predictor_model = ("shape_predictor_68_face_landmarks.dat")
face_detector = dlib.get_frontal_face_detector()
face_pose_predictor = dlib.shape_predictor(predictor_model)
face_aligner = openface.AlignDlib(predictor_model)



images = []
labels = []

cap = cv2.VideoCapture(0)
name = "hussam"

count = 1
while(True):
    _, readimage = cap.read()
    readimage = cv2.cvtColor(readimage, cv2.COLOR_BGR2GRAY)
    res = cv2.resize(readimage,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
    detected_faces = face_detector(res, 1)		
    for j, face_rect in enumerate(detected_faces):
        pose_landmarks = face_pose_predictor(res, face_rect)
        alignedFace = face_aligner.align(400, res, face_rect, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        cv2.imwrite("samples\\" + name + "\\" + name + " (" + str(count) + ").jpg", alignedFace)
    cv2.imshow('readimage', res)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    count = count + 1


    

cv2.destroyAllWindows()
cap.release()



