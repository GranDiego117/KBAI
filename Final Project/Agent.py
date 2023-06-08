# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.
# 
# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageChops
import numpy as np
import cv2


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

        def apply_transformation(image, transformation):
            if transformation == 0:  # change
                print("|| Transformation = Change")
                return image
            elif transformation == 1:  # horizontal
                print("|| Transformation = Horizontal")
                image = cv2.flip(image, 1)
            elif transformation == 2:  # vertical
                print("|| Transformation = Vertical")
                image = cv2.flip(image, 0)
            elif transformation == 3:  # rotation_90
                print("|| Transformation = rotation 90")
                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            elif transformation == 4:  # rotation_180
                print("|| Transformation = rotation 180")
                image = cv2.rotate(image, cv2.ROTATE_180)
            elif transformation == 5:  # rotation_270
                print("|| Transformation = rotation 270")
                image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            return image
        
        figure_a = problem.figures["A"]
        #image_path = figure_a.visualFilename
        problem_type = problem.problemType
        problem_hasVisual = problem.hasVisual
        problem_hasVerbal = problem.hasVerbal

        problem_images = {}
        option_images = {}

        # Tolerance in pixels for image differences
        tolerance = 500000

        # Loop over each figure in the problem.
        for name, figure in problem.figures.items():
            # Load the image file.
            image_path = figure.visualFilename
            #image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            image = cv2.imread(image_path)

            # Check if image is loaded properly
            if image is None:
                print(f"Error loading image {image_path}")
                continue  # Skip this iteration and go to next figure


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

            # Check if there is any change at all between A and B, and A and C
            AB_change = np.sum(cv2.absdiff(A, B)) == 0
            AC_change = np.sum(cv2.absdiff(A, C)) == 0

            # Check for horizontal reflection similarity
            AB_horizontal = np.sum(cv2.absdiff(A, cv2.flip(B, 1))) < tolerance
            AC_horizontal = np.sum(cv2.absdiff(A, cv2.flip(C, 1))) < tolerance


            # Check for vertical reflection similarity
            AB_vertical = np.sum(cv2.absdiff(A, cv2.flip(B, 0))) < tolerance
            AC_vertical = np.sum(cv2.absdiff(A, cv2.flip(C, 0))) < tolerance


            # Check for rotation similarity
            AB_rotation = [np.sum(cv2.absdiff(A, cv2.rotate(B, rot))) < tolerance for rot in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]]
            AC_rotation = [np.sum(cv2.absdiff(A, cv2.rotate(C, rot))) < tolerance for rot in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]]

            # Check if contours are similar between A and B
            AB_contour = np.sum(cv2.absdiff(A, B)) < tolerance
            # Check if contours are similar between A and C
            AC_contour = np.sum(cv2.absdiff(A, C)) < tolerance

            # Create a list to hold the sequence of transformations that would take B to A and C to A
            transformations_to_apply = []
            transformations_difference = []

            transformations_difference.append(f"AB_change: {np.sum(cv2.absdiff(A, B))}")
            transformations_difference.append(f"AC_change: {np.sum(cv2.absdiff(A, C))}")
            transformations_difference.append(f"AB_horizontal: {np.sum(cv2.absdiff(A, cv2.flip(B, 1)))}")
            transformations_difference.append(f"AC_horizontal:  {np.sum(cv2.absdiff(A, cv2.flip(C, 1)))}")
            transformations_difference.append(f"AB_vertical: {np.sum(cv2.absdiff(A, cv2.flip(B, 0)))}")
            transformations_difference.append(f"AC_vertical: {np.sum(cv2.absdiff(A, cv2.flip(C, 0)))}")

            #cv2.imshow('A', A)
            #cv2.imshow('A flipped', cv2.flip(A,1))
            #cv2.imshow('C', C)
            #flipped_B = cv2.flip(B, 1)
            #diff_AB = cv2.absdiff(A, flipped_B)
            #cv2.imshow('Difference between A and flipped B', diff_AB)
            #cv2.waitKey(0)
            
            transformations_to_apply_AB = []
            transformations_to_apply_AC = []

            # Determine the transformations to apply
            if AB_change:
                transformations_to_apply.append('Change not detected between A and B')
                transformations_to_apply_AB.append(0)
            if AC_change:
                transformations_to_apply.append('Change not detected between A and C')
                transformations_to_apply_AC.append(0)
            if AB_horizontal:
                transformations_to_apply.append('Horizontal Reflection between A and B')
                transformations_to_apply_AB.append(1)
            if AC_horizontal:
                transformations_to_apply.append('Horizontal Reflection between A and C')
                transformations_to_apply_AC.append(1)
            if AB_vertical:
                transformations_to_apply.append('Vertical Reflection between A and B')
                transformations_to_apply_AB.append(2)
            if AC_vertical:
                transformations_to_apply.append('Vertical Reflection between A and C')
                transformations_to_apply_AC.append(2)
            #for i, degree in enumerate([90, 180, 270]):
            #    if AB_rotation[i] == 1:
            #        transformations_to_apply.append(f'Rotation by {degree} degrees between A and B')
            #        transformations_to_apply_AB.append(3 + i)
            #    if AC_rotation[i] == 1:
            #        transformations_to_apply.append(f'Rotation by {degree} degrees between A and C')
            #        transformations_to_apply_AC.append(3 + i)
           # if AB_contour:
           #     transformations_to_apply.append('Same contours between A and B')
           # if AC_contour:
           #     transformations_to_apply.append('Same contours between A and C')

            print(image_path)#, 'To find the image for quadrant D, apply these transformations: ', transformations_to_apply)
            print('\n'.join(transformations_difference))
            print('\n'.join(transformations_to_apply))

             # Try to apply the transformations from A->B to C->D and A->C to B->D
            print("===================================")
            for option, D in option_images.items():
                print(" Option: ", option, " # of B->D Transformations expected: ", len(transformations_to_apply_AB), " # of C->D transformations expected: ", len(transformations_to_apply_AC))
            
            # Initialize counters for successful transformations
                success_count_AB = 0
                success_count_AC = 0
                # Apply each transformation from A to B on image C
                for transformation in transformations_to_apply_AB:
                    transformed_C = apply_transformation(C, transformation)
                    print("Transformation C->D: ", transformation, " Transformation difference: ", np.sum(cv2.absdiff(transformed_C, D)))
                    if np.sum(cv2.absdiff(transformed_C, D)) < tolerance:
                        success_count_AB += 1
                        print("Transformation C->D: ", transformation, " # of transformations analyzed: ", success_count_AB)

                # Apply each transformation from A to C on image B
                for transformation in transformations_to_apply_AC:
                    transformed_B = apply_transformation(B, transformation)
                    print("Transformation B->D: ", transformation, " Transformation difference: ", np.sum(cv2.absdiff(transformed_B, D)))
                    if np.sum(cv2.absdiff(transformed_B, D)) < tolerance:
                        success_count_AC += 1
                        print("Transformation B->D: ", transformation, " # of transformations analyzed: ", success_count_AC)

                # If the number of successful transformations equals the total number of transformations, we found our image
                if success_count_AB == len(transformations_to_apply_AB) and success_count_AC == len(transformations_to_apply_AC):
                    print("Answer: ", int(option))
                    print("===================================")
                    input("Press Enter to continue...")
                    return int(option)
            
            print("No solution")
            print("===================================")
            input("Press Enter to continue...")

            


        # If problem is 3x3
        #elif problem.problemType == "3x3":
            #print('This is a 3x3 problem')


        #print("Path: ", image_path, " type: ", problem_type, " visual: ", problem_hasVisual, " verbal: ", problem_hasVerbal)
        return -1