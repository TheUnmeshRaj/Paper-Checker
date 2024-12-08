import cv2
import numpy as np

import utils


def process_rectangle(img, rect_points, answers, questions=5, choices=5):
    """Process a single OMR rectangle."""
    width, height = 700, 700
    rect_points = utils.reorder(rect_points)  
    pts1 = np.float32(rect_points)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])  
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (width, height))
    imgWarpColored = cv2.warpPerspective(img, matrix, (width, height))  

    
    cv2.drawContours(img, rect_points, -1, (255, 0, 0), 20)  
    rect_points = utils.reorder(rect_points)  
    ptsG1 = np.float32(rect_points)  
    ptsG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])  
    matrixG = cv2.getPerspectiveTransform(ptsG1, ptsG2)  
    imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150))  

    
    imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)  
    imgThresh = cv2.threshold(imgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]  

    try:
        boxes = utils.splitBoxes(imgThresh)  
    except TypeError:
        print("Fixing splitBoxes call: Adjusting split logic.")
        boxes = utils.splitBoxes(imgThresh, questions, choices)

    pixel_values = np.zeros((questions, choices))
    for i, box in enumerate(boxes):
        row, col = divmod(i, choices)
        pixel_values[row][col] = cv2.countNonZero(box)

    user_answers = [np.argmax(row) for row in pixel_values]  

    grading = [1 if user_answers[i] == answers[i] else 0 for i in range(questions)]

    
    utils.showAnswers(imgWarp, user_answers, grading, answers)

    return imgWarp, imgThresh, grading


pathImage = "1.jpg"
heightImg, widthImg = 700, 700
questions, choices = 5, 5

answers_list = [
    [0, 1, 3, 2, 1],  
    [0, 4, 2, 1, 2],  
    [1, 1, 2, 2, 3],  
    [2, 1, 3, 2, 2],  
    [2, 3, 4, 2, 4]   
]

img = cv2.imread(pathImage)
img = cv2.resize(img, (widthImg, heightImg))
imgContours = img.copy()
imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
imgCanny = cv2.Canny(imgBlur, 10, 70)

contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
rectContours = utils.rectContours(contours)

original_images = []
corrected_images = []
final_grades = []

for i in range(5):  
    try:
        rect_points = rectContours[i]
        imgWarp, imgThresh, grading = process_rectangle(img, rect_points, answers_list[i], questions, choices)
        original_images.append(cv2.drawContours(img.copy(), [rect_points], -1, (0, 255, 0), 10))
        corrected_images.append(imgWarp)
        final_grades.append(sum(grading) / len(grading) * 100)
    except IndexError:
        print(f"Rectangle {i + 1} could not be processed. Skipping.")
        original_images.append(imgBlank)
        corrected_images.append(imgBlank)

top_row = utils.stackImage(original_images, 0.3)
bottom_row = utils.stackImage(corrected_images, 0.3)
final_image = np.vstack([top_row, bottom_row])


utils.showAnswers(imgWarp, user_answers, grading, answers_list[i])  
utils.drawGrid(imgWarp)  

imgRawDrawings = np.zeros_like(imgWarp)  
utils.showAnswers(imgRawDrawings, user_answers, grading, answers_list[i])  


pts1 = np.float32(rect_points)
pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
invMatrix = cv2.getPerspectiveTransform(pts2, pts1)  
imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (widthImg, heightImg))  


imgRawGrade = np.zeros_like(imgGradeDisplay, np.uint8)  
score = sum(grading) / len(grading) * 100  
cv2.putText(imgRawGrade, str(int(score)) + "%", (70, 100),
            cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 255), 3)  


invMatrixG = cv2.getPerspectiveTransform(ptsG2, ptsG1)  
imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg, heightImg))  # INV IMAGE WARP

# SHOW ANSWERS AND GRADE ON FINAL IMAGE
imgFinal = cv2.addWeighted(imgWarp, 1, imgInvWarp, 1, 0)
imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1, 0)

# Display the results
cv2.imshow("Final OMR Results", final_image)
cv2.imshow("Final Result", imgFinal)
cv2.waitKey(0)
cv2.destroyAllWindows()
