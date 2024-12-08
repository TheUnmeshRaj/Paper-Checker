import cv2
import numpy as np

import util

path = "1.jpg"
widthImage = 700
heightImage = 700

# DEFINING ALL THE IMAGES THAT ARE USED IN THE PIPELINE
img = cv2.imread(path)
img = cv2.resize(img,(widthImage,heightImage))
imgContours = img.copy()
imgBiggestContours = img.copy()
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
imgCanny = cv2.Canny(imgBlur,10,50)

try:
  # GET THE COnTOURS
  contours,hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
  cv2.drawContours(imgContours,contours,-1,(0,255,0),1)

  # FINDING RECTANGLES
  rectContour = util.rectContours(contours)
  PartA = rectContour[0]
  PartB = rectContour[1]

  if PartA.size != 0 and PartB.size != 0:
    PartA=util.reorder(PartA)
    cv2.drawContours(imgBiggestContours,PartA,-1,(0,255,0),10)
    pts1 = np.float32(PartA) 
    pts2 = np.float32([[0, 0],[widthImage, 0], [0, heightImage],[widthImage, heightImage]]) 
    matrix = cv2.getPerspectiveTransform(pts1, pts2) 
    imgWarpA = cv2.warpPerspective(img, matrix, (widthImage, heightImage)) 
    
    PartB=util.reorder(PartB)
    cv2.drawContours(imgBiggestContours,PartB,-1,(0,0,255),10)
    ptsB1 = np.float32(PartB) 
    ptsB2 = np.float32([[0, 0],[widthImage, 0], [0, heightImage],[widthImage, heightImage]]) 
    matrixB = cv2.getPerspectiveTransform(ptsB1, ptsB2) 
    imgWarpB = cv2.warpPerspective(img, matrixB, (widthImage, heightImage)) 
    
    # APPLY THRESHOLD
    imgWarpGrayA = cv2.cvtColor(imgWarpA,cv2.COLOR_BGR2GRAY)
    imgThreshA = cv2.threshold(imgWarpGrayA,180,255,cv2.THRESH_BINARY_INV)[1]
    
    imgWarpGrayB = cv2.cvtColor(imgWarpB,cv2.COLOR_BGR2GRAY)
    imgThreshB = cv2.threshold(imgWarpGrayB,180,255,cv2.THRESH_BINARY_INV)[1]
    
    imgBlank = np.zeros_like(img)
    imageArray = ([img,imgGray,imgCanny,imgContours],
              [imgBiggestContours,imgThreshA,imgThreshB,imgBlank])
    
    boxes = util.splitBoxes(imgThreshB)
    cv2.imshow("Test",boxes[0])
    cv2.imshow("Test",boxes[1])
    cv2.imshow("Test",boxes[2])
    cv2.imshow("Test",boxes[3])
except:
  imgBlank = np.zeros_like(img)
  imageArray = ([img,imgGray,imgCanny,imgContours],
               [imgBlank, imgBlank, imgBlank, imgBlank])


labels = [["Original","Gray","Edges","Contours"],
            ["Biggest Contour","PART A","PART B","Final"]]

imgStacked = util.stackImage(imageArray,0.5,labels)
cv2.imshow("All",imgThreshB)
cv2.waitKey(0)