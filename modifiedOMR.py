import cv2
import numpy as np

import utils


def process_rectangle(img, rect_points, answers, questions=5, choices=5):
    """Process and overlay corrections on a single OMR rectangle."""
    width, height = 700, 700

    # Reorder points and warp perspective
    rect_points = utils.reorder(rect_points)
    pts1 = np.float32(rect_points)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (width, height))

    # Grayscale and threshold
    imgWarpColoredGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWarpColoredGray, 170, 255, cv2.THRESH_BINARY_INV)[1]

    # Split boxes and count pixel values
    boxes = utils.splitBoxes(imgThresh)
    pixel_values = np.zeros((questions, choices))
    for i, box in enumerate(boxes):
        row, col = divmod(i, choices)
        pixel_values[row][col] = cv2.countNonZero(box)

    # Get user answers and grading
    user_answers = [np.argmax(row) for row in pixel_values]
    grading = [1 if user_answers[i] == answers[i] else 0 for i in range(questions)]

    # Draw answers (with color scheme) on the warped image
    utils.showAnswers(imgWarpColored, user_answers, grading, answers)

    # Prepare overlay corrections
    imgRawDrawings = np.zeros_like(imgWarpColored)
    utils.showAnswers(imgRawDrawings, user_answers, grading, answers)

    # Warp corrected drawing back to original perspective
    invMatrix = cv2.getPerspectiveTransform(pts2, pts1)
    imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (img.shape[1], img.shape[0]))

    return imgInvWarp, grading


# Main Code
pathImage = "1.jpg"
heightImg, widthImg = 700, 700
questions, choices = 5, 5

# Correct answers for each rectangle
answers_list = [
    [1, 3, 2, 1, 4],
    [2, 1, 4, 3, 0],
    [0, 2, 3, 4, 1],
    [4, 4, 4, 4, 4],
    [1, 1, 1, 1, 1]
]

# Load and preprocess the image
img = cv2.imread(pathImage)
img = cv2.resize(img, (widthImg, heightImg))
imgContours = img.copy()

# Grayscale, blur, and edge detection
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
imgCanny = cv2.Canny(imgBlur, 10, 70)

# Find contours and get rectangles
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
rectContours = utils.rectContours(contours)

# Process and overlay corrections for each rectangle
imgFinal = img.copy()
for i in range(min(5, len(rectContours))):
    try:
        rect_points = rectContours[i]
        imgInvWarp, grading = process_rectangle(img, rect_points, answers_list[i], questions, choices)
        imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
    except IndexError:
        print(f"Rectangle {i+1} could not be processed. Skipping.")

# Display the final image
cv2.imshow("Final OMR Results", imgFinal)
cv2.waitKey(0)
cv2.destroyAllWindows()
