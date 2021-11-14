'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1b.py
# Functions:		applyPerspectiveTransform, detectMaze, writeToCsv
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)               ##
##############################################################
import numpy as np
import cv2
import csv


##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################


##############################################################


def applyPerspectiveTransform(input_img):

	if(len(input_img.shape)==3):
		gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
	
		kernel = np.ones((2, 2), np.uint8)
		_, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
		closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
		edged = cv2.Canny(closed, 170, 255)
		_, threshold = cv2.threshold(edged, 120, 255, cv2.THRESH_BINARY)
		contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		contour = contours[0]
		approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
		y=1
		while len(approx) != 4:
			contour = contours[y]
			approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
			y+=1
		n = approx.ravel()

		for x in range(0, 7, 2):
			cv2.circle(input_img, (n[x], n[x + 1]), 1, (0, 255, 0), 2)

		pts = np.float32([[n[0], n[1]], [n[2], n[3]], [n[4], n[5]], [n[6], n[7]]])
		rect = np.zeros((4, 2), dtype="float32")
		s = pts.sum(axis=1)
		rect[0] = pts[np.argmin(s)]
		rect[2] = pts[np.argmax(s)]
		diff = np.diff(pts, axis=1)
		rect[1] = pts[np.argmin(diff)]
		rect[3] = pts[np.argmax(diff)]

		(tl, tr, br, bl) = rect
		dst = np.array([
			[0, 0],
			[1280, 0],
			[1280, 1280],
			[0, 1280]], dtype="float32")
		M = cv2.getPerspectiveTransform(rect, dst)
		warped = cv2.warpPerspective(input_img, M, (1280, 1280))
		return warped
	
	else:
		num = 1280
		ret , masked_img = cv2.threshold(cv2.GaussianBlur(input_img,(5,5),0),0,255,cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
		contours , hierarchy = cv2.findContours(masked_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		epsilon = 0.1*cv2.arcLength(contours[1],True)
		approx = cv2.approxPolyDP(contours[1],epsilon,True)
		pts1 = np.squeeze(np.array(approx))
		pts2 = [[0,0],[0,0],[0,0],[0,0]]
		for i in range(4):
			item = pts1[i]
			if(item[0]<200):
				pts2[i][0] = 0
			else:
				pts2[i][0] = num
			if(item[1]<200):
				pts2[i][1] = 0
			else:
				pts2[i][1] = num
		pts1 = np.float32(pts1)
		pts2 = np.float32(np.array(pts2))
		matrix = cv2.getPerspectiveTransform(pts1,pts2) 
		warped_img = cv2.morphologyEx(cv2.warpPerspective(masked_img,matrix,(num,num)),cv2.MORPH_OPEN,np.ones((5,5,)))
		return warped_img


def detectMaze(warped):
	kernel = np.ones((5, 5), np.uint8)
	eroded = cv2.erode(warped, kernel, 5)
	warped = cv2.morphologyEx(eroded, cv2.MORPH_OPEN, kernel)
	gray1 = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	_, final = cv2.threshold(gray1, 120, 255, cv2.THRESH_BINARY)

	end_h = 1280
	end_w = 1280

	unit_h = int(end_h / 10)
	unit_w = int(end_w / 10)

	list = []
	dict = {0: 1, 255: 0}

	for i in range(0, end_h + unit_h, unit_h):
		for j in range(0, end_w, unit_w):
			coordinate = [i, j]
			h0 = coordinate[0]
			w0 = coordinate[1]
			h = (coordinate[0] + unit_h)
			w = (coordinate[1] + unit_w)

			if (h and h0) < end_h and (w and w0) < end_w:
				list.append((h0, w0, h, w))
	y = 0
	result = []
	maze_array = []

	for x in range(0, len(list)):
		h0, w0, h, w = list[x]
		block = final[h0:h, w0:w]
		size = block.shape

		if size[0] <= unit_h and size[1] <= unit_w:
			for a in range(10):
				if block[0 + a, (size[1] // 2)] == 0:
					north = 2
					break
				else:
					north = 0
			for a in range(2, 10):
				if block[size[0] - a, size[1] // 2] == 0:
					south = 8
					break
				else:
					south = 0
			for a in range(10):
				if block[size[0] // 2, 0 + a] == 0:
					west = 1
					break
				else:
					west = 0
			for a in range(2, 10):
				if block[size[0] // 2, size[1] - a] == 0:
					east = 4
					break
				else:
					east = 0
			edge = north + south + west + east

			if y < 9:
				result.append(edge)
				y += 1
			elif y == 9:
				result.append(edge)
				maze_array.append(result)
				result = []
				y = 0
		else:
			pass

	return maze_array


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def writeToCsv(csv_file_path, maze_array):
	"""
	Purpose:
	---
	takes the encoded maze array and csv file name as input and writes the encoded maze array to the csv file

	Input Arguments:
	---
	`csv_file_path` :	[ str ]
		file path with name for csv file to write

	`maze_array` :		[ nested list of lists ]
		encoded maze in the form of a 2D array

	Example call:
	---
	warped_img = writeToCsv('test_cases/maze00.csv', maze_array)
	"""

	with open(csv_file_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(maze_array)


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
# 					as input, applies Perspective Transform by calling applyPerspectiveTransform function,
# 					encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
# 					by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
# 					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
# 					applyPerspectiveTransform and detectMaze functions.

if __name__ == "__main__":

	# path directory of images in 'test_cases' folder
	img_dir_path = 'test_cases/'

	# path to 'maze00.jpg' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

	print('\n============================================')
	print('\nFor maze0' + str(file_num) + '.jpg')

	# path for 'maze00.csv' output file
	csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'

	# read the 'maze00.jpg' image file
	input_img = cv2.imread(img_file_path)

	# get the resultant warped maze image after applying Perspective Transform
	warped_img = applyPerspectiveTransform(input_img)

	if type(warped_img) is np.ndarray:

		# get the encoded maze in the form of a 2D array
		maze_array = detectMaze(warped_img)

		if (type(maze_array) is list) and (len(maze_array) == 10):

			print('\nEncoded Maze Array = %s' % (maze_array))
			print('\n============================================')

			# writes the encoded maze array to the csv file
			writeToCsv(csv_file_path, maze_array)

			cv2.imshow('warped_img_0' + str(file_num), warped_img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		else:

			print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
			exit()

	else:

		print(
			'\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
		exit()

	choice = input('\nDo you want to run your script on all maze images ? => "y" or "n": ')

	if choice == 'y':

		for file_num in range(1, 10):

			# path to image file
			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')
			print('\nFor maze0' + str(file_num) + '.jpg')

			# path for csv output file
			csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'

			# read the image file
			input_img = cv2.imread(img_file_path)

			# get the resultant warped maze image after applying Perspective Transform
			warped_img = applyPerspectiveTransform(input_img)

			if type(warped_img) is np.ndarray:

				# get the encoded maze in the form of a 2D array
				maze_array = detectMaze(warped_img)

				if (type(maze_array) is list) and (len(maze_array) == 10):

					print('\nEncoded Maze Array = %s' % (maze_array))
					print('\n============================================')

					# writes the encoded maze array to the csv file
					writeToCsv(csv_file_path, maze_array)

					cv2.imshow('warped_img_0' + str(file_num), warped_img)
					cv2.waitKey(0)
					cv2.destroyAllWindows()

				else:

					print(
						'\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
					exit()

			else:

				print(
					'\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
				exit()

	else:

		print('')
