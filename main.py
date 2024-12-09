import cv2
import numpy as np

import utils


def process_rectangle(img, rect_points, answers, questions=5, choices=5):
    """Process a single OMR rectangle and calculate grades."""
    width, height = 700, 700
    rect_points = utils.reorder(rect_points)
    pts1 = np.float32(rect_points)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (width, height))

    imgWarpColoredGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWarpColoredGray, 170, 255, cv2.THRESH_BINARY_INV)[1]
    boxes = utils.splitBoxes(imgThresh)

    pixel_values = np.zeros((questions, choices))
    for i, box in enumerate(boxes):
        row, col = divmod(i, choices)
        pixel_values[row][col] = cv2.countNonZero(box)

    user_answers = [np.argmax(row) for row in pixel_values]

    grading = [1 if user_answers[i] == answers[i] else 0 for i in range(questions)]
    score = sum([2 if grading[i] == 1 else -0.5 for i in range(questions)])

    imgRawDrawings = np.zeros_like(imgWarpColored)
    utils.showAnswers(imgRawDrawings, user_answers, grading, answers)

    invMatrix = cv2.getPerspectiveTransform(pts2, pts1)
    imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (widthImg, heightImg))
    imgFinal = cv2.addWeighted(img, 1, imgInvWarp, 1, 0)

    return imgFinal, grading, score


pathImage = "1.jpg"
heightImg, widthImg = 700, 700
questions, choices = 5, 5

SetA = [
    [2, 3, 4, 2, 3],  # Part A - 1-5
    [1, 3, 2, 2, 1],  # Part A - 11-15
    [2, 3, 4, 3, 2],  # Part A - 6-10
    [1, 3, 3, 2, 3],  # Part B - 1-5
    [2, 2, 3, 2, 3]   # Part B - 6-10
]

img = cv2.imread(pathImage)
img = cv2.resize(img, (widthImg, heightImg))
imgContours = img.copy()

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
imgCanny = cv2.Canny(imgBlur, 10, 70)

contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
rectContours = utils.rectContours(contours)

scores = []
imgFinal = img.copy()

for i in range(5):
    try:
        rect_points = rectContours[i]
        imgFinal, grading, score = process_rectangle(imgFinal, rect_points, SetA[i], questions, choices)
        scores.append(score)
    except IndexError:
        print(f"Rectangle {i+1} could not be processed. Skipping.")
        scores.append(0)

part_a_score = sum(scores[:3])  # Rectangles 1, 2, 3
part_b_score = sum(scores[3:])  # Rectangles 4, 5
cv2.putText(imgFinal, f"Part A Score = {part_a_score:.2f}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
cv2.putText(imgFinal, f"Part B Score = {part_b_score:.2f}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

cv2.imshow("Final OMR Results", imgFinal)

print(f"Part A Score: {part_a_score:.2f}")
print(f"Part B Score: {part_b_score:.2f}")

cv2.waitKey(0)
cv2.destroyAllWindows()
