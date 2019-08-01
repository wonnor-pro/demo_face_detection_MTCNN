import cv2 

capture = cv2.VideoCapture(0)

while True:
	_, frame = capture.read()
	grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	restore = cv2.cvtColor(grayFrame,cv2.COLOR_GRAY2BGR)
	cv2.imshow('video gray', grayFrame)
	cv2.imshow('video original', frame)
	cv2.imshow('restore', restore)

	if cv2.waitKey(1)==27:
		break

capture.release()
cv2.destroyAllWindows()