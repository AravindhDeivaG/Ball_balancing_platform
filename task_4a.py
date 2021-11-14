'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 4A of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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
# Filename:			task_4a.py
# Functions:		find_path, read_start_end_coordinates
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the six available   ##
## modules for this task (numpy, opencv, os, traceback,     ##
## sys, json)												##
##############################################################
import numpy as np
import cv2
import os
import traceback
import sys
import json

# Import 'task_1b.py' file as module
try:
    import task_1b

except ImportError:
    print('\n[ERROR] task_1b.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_1b.py is present in this current directory.\n')
    sys.exit()

except Exception as e:
    print('Your task_1b.py throwed an Exception, kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)
    sys.exit()


##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

def check_allowable_path(coord, maze_array):  # To determine the directions in which walls are present
    N_wall = S_wall = E_wall = W_wall = False
    combination = []
    numbers = [1, 2, 4, 8]

    def subset_sum(numbers, target, partial=[]):  # decode values of wall from maze_array element
        s = sum(partial)
        if s == target:
            combination.extend(partial)
        if s >= target:
            return
        for i in range(len(numbers)):
            n = numbers[i]
            remaining = numbers[i + 1:]
            subset_sum(remaining, target, partial + [n])
        return combination

    val = subset_sum(numbers, maze_array[coord[0]][coord[1]])
    if val is None:
        N_wall = S_wall = E_wall = W_wall = False
    else:
        if 1 in val:
            W_wall = True
        if 2 in val:
            N_wall = True
        if 4 in val:
            E_wall = True
        if 8 in val:
            S_wall = True
    return N_wall, S_wall, E_wall, W_wall


##############################################################


def find_path(maze_array, start_coord, end_coord):
    """
    Purpose:
    ---
    Takes a maze array as input and calculates the path between the
    start coordinates and end coordinates.

    Input Arguments:
    ---
    `maze_array` :   [ nested list of lists ]
        encoded maze in the form of a 2D array

    `start_coord` : [ tuple ]
        start coordinates of the path

    `end_coord` : [ tuple ]
        end coordinates of the path

    Returns:
    ---
    `path` :  [ list of tuples ]
        path between start and end coordinates

    Example call:
    ---
    path = find_path(maze_array, start_coord, end_coord)
    """

    path = None

    ################# ADD YOUR CODE HERE #################

    already_visited = []

    def search_way(current, path=[]):
        N_wall, S_wall, E_wall, W_wall = check_allowable_path(current, maze_array)
        neighbour = []
        if (N_wall == False) and (current[0] - 1, current[1]) not in already_visited:
            adjacent = (current[0] - 1, current[1])
            neighbour.append(adjacent)

        if (S_wall == False) and (current[0] + 1, current[1]) not in already_visited:
            adjacent = (current[0] + 1, current[1])
            neighbour.append(adjacent)

        if (W_wall == False) and (current[0], current[1] - 1) not in already_visited:
            adjacent = (current[0], current[1] - 1)
            neighbour.append(adjacent)

        if (E_wall == False) and (current[0], current[1] + 1) not in already_visited:
            adjacent = (current[0], current[1] + 1)
            neighbour.append(adjacent)

        if current not in already_visited:
            already_visited.append(current)
            path.append(current)
        if current != end_coord:
            if len(neighbour) != 0:
                for n in neighbour:
                    already_visited.append(n)
                    path.append(n)
                    path = search_way(n, path)
            if len(neighbour) == 0:
                if len(path) != 1:
                    path.pop()
                    current = path[-1]
                    path = search_way(current, path)
                else:
                    path.pop()
                    return path

        if current == end_coord:
            return path

        return path

    final = search_way(start_coord)
    path = []
    for i in final:
        if i not in path:
            path.append(i)

    if len(final) == 0:
        path = None

    return path

    ######################################################


def read_start_end_coordinates(file_name, maze_name):
    """
    Purpose:
    ---
    Reads the corresponding start and end coordinates for each maze image
    from the specified JSON file

    Input Arguments:
    ---
    `file_name` :   [ str ]
        name of JSON file

    `maze_name` : [ str ]
        specify the maze image for which the start and end coordinates are to be returned.

    Returns:
    ---
    `start_coord` : [ tuple ]
        start coordinates for the maze image

    `end_coord` : [ tuple ]
        end coordinates for the maze image

    Example call:
    ---
    start, end = read_start_end_coordinates("start_end_coordinates.json", "maze00")
    """

    start_coord = None
    end_coord = None

    ################# ADD YOUR CODE HERE #################
    with open(file_name) as f:
        data = json.load(f)
    start_coord = tuple(data[maze_name]["start_coord"])
    end_coord = tuple(data[maze_name]["end_coord"])

    ######################################################

    return start_coord, end_coord


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
# 					as input and reads the corresponding start and end coordinates for this image from 'start_end_coordinates.json'
# 					file by calling read_start_end_coordinates function. It then applies Perspective Transform
# 					by calling applyPerspectiveTransform function, encodes the maze input in form of 2D array
# 					by calling detectMaze function and finds the path between start, end coordinates by calling
# 					find_path function. It then asks the user whether to repeat the same on all maze images
# 					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
# 					read_start_end_coordinates and find_path functions.
if __name__ == "__main__":

    # path directory of images in 'test_cases' folder
    img_dir_path = 'test_cases/'

    file_num = 0

    maze_name = 'maze0' + str(file_num)

    # path to 'maze00.jpg' image file
    img_file_path = img_dir_path + maze_name + '.jpg'

    # read start and end coordinates from json file
    start_coord, end_coord = read_start_end_coordinates("start_end_coordinates.json", maze_name)

    print('\n============================================')
    print('\nFor maze0' + str(file_num) + '.jpg')

    # read the 'maze00.jpg' image file
    input_img = cv2.imread(img_file_path)

    # get the resultant warped maze image after applying Perspective Transform
    warped_img = task_1b.applyPerspectiveTransform(input_img)

    if type(warped_img) is np.ndarray:

        # get the encoded maze in the form of a 2D array
        maze_array = task_1b.detectMaze(warped_img)

        if (type(maze_array) is list) and (len(maze_array) == 10):

            print('\nEncoded Maze Array = %s' % (maze_array))
            print('\n============================================')

            path = find_path(maze_array, start_coord, end_coord)

            if (type(path) is list):

                print('\nPath calculated between %s and %s is %s' % (start_coord, end_coord, path))
                print('\n============================================')

            else:
                print('\n Path does not exist between %s and %s' % (start_coord, end_coord))

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

            maze_name = 'maze0' + str(file_num)

            img_file_path = img_dir_path + maze_name + '.jpg'

            # read start and end coordinates from json file
            start_coord, end_coord = read_start_end_coordinates("start_end_coordinates.json", maze_name)

            print('\n============================================')
            print('\nFor maze0' + str(file_num) + '.jpg')

            # read the 'maze00.jpg' image file
            input_img = cv2.imread(img_file_path)

            # get the resultant warped maze image after applying Perspective Transform
            warped_img = task_1b.applyPerspectiveTransform(input_img)

            if type(warped_img) is np.ndarray:

                # get the encoded maze in the form of a 2D array
                maze_array = task_1b.detectMaze(warped_img)

                if (type(maze_array) is list) and (len(maze_array) == 10):

                    print('\nEncoded Maze Array = %s' % (maze_array))
                    print('\n============================================')

                    path = find_path(maze_array, start_coord, end_coord)

                    if (type(path) is list):

                        print('\nPath calculated between %s and %s is %s' % (start_coord, end_coord, path))
                        print('\n============================================')

                    else:
                        print('\n Path does not exist between %s and %s' % (start_coord, end_coord))

                else:
                    print(
                        '\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
                    exit()

            else:
                print(
                    '\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
                exit()

    else:
        print()
