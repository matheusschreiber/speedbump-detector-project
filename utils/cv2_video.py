import cv2

video = cv2.VideoCapture(0)

if (video.isOpened() == False):
	print("Error reading video file")

frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)
result = cv2.VideoWriter('output.mp4',
						cv2.VideoWriter_fourcc(*'XVID'),
						10, size)
	
while(True):
	ret, frame = video.read()
	if ret == True:
		
		cv2.rectangle(frame, (50,50), (100, 100), (0, 0, 255),2)
		cv2.putText(frame, '95.4%', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		result.write(frame)
		cv2.imshow('Frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('s'):
			break

	else:
		break
video.release()
result.release()
cv2.destroyAllWindows()
print("The video was successfully saved")

