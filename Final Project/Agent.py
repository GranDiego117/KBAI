# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageOps
import numpy as np
import cv2 as cv


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        
        figure_a = problem.figures["A"]
        #image_path = figure_a.visualFilename
        problem_type = problem.problemType
        problem_hasVisual = problem.hasVisual
        problem_hasVerbal = problem.hasVerbal

        problem_images = {}
        option_images = {}

        # Loop over each figure in the problem.
        for name, figure in problem.figures.items():
            # Load the image file.
            image_path = figure.visualFilename
            image = Image.open(image_path)

            # If the name is a letter, add it to the problem images. 
            if name.isalpha():
                problem_images[name] = image
            # If the name is a number, add it to the options images.
            elif name.isdigit():
                option_images[name] = image

        # If problem is 2x2
        if problem.problemType == "2x2":
            # Extract the individual images
            A = problem_images.get('A')
            B = problem_images.get('B')
            C = problem_images.get('C')

            # Variables to store comparison results
            AB_horizontal = AC_horizontal = AB_vertical = AC_vertical = 0
            AB_rotation = AC_rotation = [0, 0, 0]  # For 90, 180, 270 degrees respectively

            # Check for horizontal reflection similarity between A and B
            if np.array_equal(np.array(A), np.array(ImageOps.mirror(B))):
                AB_horizontal = 1

            # Check for horizontal reflection similarity between A and C
            if np.array_equal(np.array(A), np.array(ImageOps.mirror(C))):
                AC_horizontal = 1
                
            # Check for vertical reflection similarity between A and B
            if np.array_equal(np.array(A), np.array(ImageOps.flip(B))):
                AB_vertical = 1

            # Check for vertical reflection similarity between A and C
            if np.array_equal(np.array(A), np.array(ImageOps.flip(C))):
                AC_vertical = 1

            # Check for rotation similarity
            for i, degree in enumerate([90, 180, 270]):
                rotated_B = B.rotate(degree)
                rotated_C = C.rotate(degree)
                if np.array_equal(np.array(A), np.array(rotated_B)):
                    AB_rotation[i] = 1
                if np.array_equal(np.array(A), np.array(rotated_C)):
                    AC_rotation[i] = 1

            # Find contours in the images
            contours1, _ = cv.findContours(cv.cvtColor(np.array(A), cv.COLOR_BGR2GRAY), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            contours2, _ = cv.findContours(cv.cvtColor(np.array(B), cv.COLOR_BGR2GRAY), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            contours3, _ = cv.findContours(cv.cvtColor(np.array(C), cv.COLOR_BGR2GRAY), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            # Check if contours are similar between A and B
            AB_contour = cv.matchShapes(contours1[0], contours2[0], 1, 0.0)
            # Check if contours are similar between A and C
            AC_contour = cv.matchShapes(contours1[0], contours3[0], 1, 0.0)

            # Create a list to hold the sequence of transformations that would take B to A and C to A
            transformations_to_apply = []

            # Determine the transformations to apply
            if AB_horizontal == 1:
                transformations_to_apply.append('Horizontal Reflection between A and B')
            if AC_horizontal == 1:
                transformations_to_apply.append('Horizontal Reflection between A and C')
            if AB_vertical == 1:
                transformations_to_apply.append('Vertical Reflection between A and B')
            if AC_vertical == 1:
                transformations_to_apply.append('Vertical Reflection between A and C')
            for i, degree in enumerate([90, 180, 270]):
                if AB_rotation[i] == 1:
                    transformations_to_apply.append(f'Rotation by {degree} degrees between A and B')
                if AC_rotation[i] == 1:
                    transformations_to_apply.append(f'Rotation by {degree} degrees between A and C')
            if AB_contour == 1:
                transformations_to_apply.append('Same contours between A and B')
            if AC_contour == 1:
                transformations_to_apply.append('Same contours between A and C')


            print(image_path, 'To find the image for quadrant D, apply these transformations: ', transformations_to_apply)


        # If problem is 3x3
        #elif problem.problemType == "3x3":
            #print('This is a 3x3 problem')


        #print("Path: ", image_path, " type: ", problem_type, " visual: ", problem_hasVisual, " verbal: ", problem_hasVerbal)
        return -1