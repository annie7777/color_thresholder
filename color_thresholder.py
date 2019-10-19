# HSV: H -> 0 ~ 180 S



from __future__ import print_function
import cv2
import argparse
import numpy as np

		
parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--input', help='video or image')
parser.add_argument('--path', help = 'source to input')
parser.add_argument('color_space', metavar = '<color_space>', default = 'hsv', help = "'bgr' or 'hsv' or 'lab'")
args = parser.parse_args()

max_value = 255
max_value_H = 255#360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
# window_capture_name = 'Video Capture'
window_detection_name = 'Color Thresholder'
low_H_name = 'Low H/L/B'
low_S_name = 'Low S/a/G'
low_V_name = 'Low V/b/R'
high_H_name = 'High H/L/B'
high_S_name = 'High S/a/G'
high_V_name = 'High V/b/R'

def on_low_H_thresh_trackbar(val):
	global low_H
	global high_H
	low_H = val
	low_H = min(high_H-1, low_H)
	cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
	global low_H
	global high_H
	high_H = val
	high_H = max(high_H, low_H+1)
	cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
	global low_S
	global high_S
	low_S = val
	low_S = min(high_S-1, low_S)
	cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
	global low_S
	global high_S
	high_S = val
	high_S = max(high_S, low_S+1)
	cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
	global low_V
	global high_V
	low_V = val
	low_V = min(high_V-1, low_V)
	cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
	global low_V
	global high_V
	high_V = val
	high_V = max(high_V, low_V+1)
	cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)

if args.input == 'video':
	cap = cv2.VideoCapture(args.path)
elif args.input == 'image':
	cap = cv2.imread(args.path)

def Resize(img, pseudo_color, color_mask, img_threshold):
	
	h, w = img.shape[:2]

	small_h, small_w = h//2, w//2

	img_resize = cv2.resize(img, (small_w, small_h))
	pseudo_color_resize = cv2.resize(pseudo_color, (small_w, small_h))
	color_mask_resize = cv2.resize(color_mask, (small_w, small_h))
	img_threshold_resize = cv2.resize(img_threshold, (small_w, small_h))


	return img_resize, pseudo_color_resize, color_mask_resize, img_threshold_resize

# cap = cv2.VideoCapture('outpy.avi')
# cv2.namedWindow(window_capture_name)
cv2.namedWindow(window_detection_name)
cv2.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv2.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv2.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv2.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv2.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv2.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)

while True:

	if args.input == 'video':
		ret, frame = cap.read()
	elif args.input == 'image':
		frame = cap

	if frame is None:
		break

	if args.color_space == 'bgr': 
		frame_HSV = frame
	elif args.color_space == 'hsv':
		frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	elif args.color_space == 'lab':
		frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

	frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
	
	rgb_frame_threshold = cv2.merge((frame_threshold, frame_threshold, frame_threshold))

	res = cv2.bitwise_and(frame, frame, mask = frame_threshold)

	frame_resize, frame_HSV_resize, res_resize, frame_threshold_resize = Resize(frame, frame_HSV, res, rgb_frame_threshold)

	combine = np.vstack((np.hstack((frame_resize,frame_HSV_resize)), np.hstack((res_resize ,frame_threshold_resize))))
	# cv2.imshow(window_capture_name, frame_resize)
	cv2.imshow(window_detection_name, combine)

	print('Color Space:', args.color_space)
	print(low_H_name,':', low_H, ' ', high_H_name,':', high_H)
	print(low_S_name,':', low_S, ' ', high_S_name,':', high_S)
	print(low_V_name,':', low_V, ' ', high_V_name,':', high_V)
	key = cv2.waitKey(500)
	if key == ord('q') or key == 27:
		break