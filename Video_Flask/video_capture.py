'''
# Program To Read video and Extract Frames 
import cv2 

# Function to extract frames 
def FrameCapture(path): 
	
	# Path to video file 
	vidObj = cv2.VideoCapture(path) 
	
	# Used as counter variable 
	count = 0
	
	# checks whether frames were extracted 
	success = 1
	
	while success: 
		
		# function extract frames 
		success, image = vidObj.read() 

		# Saves the frames with frame-count 
		cv2.imwrite("/Frames/frame%d.jpg" % count, image) 
		count += 1

# Calling the function 
FrameCapture('tyre_sample_video_1.mp4') 
'''
import cv2
vid = cv2.VideoCapture('bald_tyre.mp4')
success,image = vid.read()
count = 0
while success:
  vid.set(cv2.CAP_PROP_POS_MSEC,(count*1000))      
  success,image = vid.read()
  print('Read a new frame: ', success)
  cv2.imwrite("Frames/frame%d.jpg" % count, image)     # save frame as JPEG file
  count += 1
  print('Total Frames:',count)