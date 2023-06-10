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
from PIL import Image, ImageChops, ImageFont, ImageDraw
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

        def process_image(image):
            # Convert the image to grayscale and binary
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            # Find contours and hierarchy
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            return contours, hierarchy
        
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
                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE )
            elif transformation == 4:  # rotation_180
                print("|| Transformation = rotation 180")
                image = cv2.rotate(image, cv2.ROTATE_180)
            elif transformation == 5:  # rotation_270
                print("|| Transformation = rotation 270")
                image = cv2.rotate(image,  cv2.ROTATE_90_COUNTERCLOCKWISE) 
            return image
        
        # Function to detect and print the number of edges for each figure in an image
        def figure_edges(contours, image_name):
            edges_count = []
            print(f"Figures in {image_name}:")
            for i, contour in enumerate(contours):
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                num_edges = len(approx)
                print(f"Figure {i+1}: {num_edges} edges")
                # Count the number of edges
                edges_count.append(len(approx))         

            return edges_count
        

        figure_a = problem.figures["A"]
        #image_path = figure_a.visualFilename
        problem_type = problem.problemType
        problem_hasVisual = problem.hasVisual
        problem_hasVerbal = problem.hasVerbal

        problem_images = {}
        option_images = {}
        best_option = None
        best_success_count = 0

        # Tolerance in pixels for image differences
        #tolerance = 500000
        tolerance = 800000

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
            # Extract the individual images
            A = problem_images.get('A')
            B = problem_images.get('B')
            C = problem_images.get('C')

            # Find contours and hierarchy for A, B, and C
            contours_A, hierarchy_A = process_image(A)
            contours_B, hierarchy_B = process_image(B)
            contours_C, hierarchy_C = process_image(C)

            print("Hierarchy A: ", hierarchy_A, "Hierarchy B: ", hierarchy_B)

            edgesA = figure_edges(contours_A, 'A')
            edgesB = figure_edges(contours_B, 'B')
            edgesC = figure_edges(contours_C, 'C')

            if sum(edgesA) > sum(edgesB):
                edgesAB = 1
            elif sum(edgesA) < sum(edgesB):
                edgesAB = -1
            else:
                edgesAB = 0

            if sum(edgesA) > sum(edgesC):
                edgesAC = 1
            elif sum(edgesA) < sum(edgesC):
                edgesAC = -1
            else:
                edgesAC = 0
 

            # Compare the hierarchies
            differencesAB = []
            differencesAC = []
            hierarchyAB = 0
            hierarchyAC = 0

            elementsAB = len(hierarchy_A[0]) - len(hierarchy_B[0])
            elementsAC = len(hierarchy_A[0]) - len(hierarchy_C[0])

            # Check if hierarchy A has fewer elements than hierarchy B
            if len(hierarchy_A[0]) < len(hierarchy_B[0]):
                num_extra_elementsAB = len(hierarchy_B[0]) - len(hierarchy_A[0])
                extra_elementsAB = [i for i in range(len(hierarchy_B[0])) if i >= len(hierarchy_A[0])]
                if len(extra_elementsAB) > 1:
                    extra_elementsAB_str = ", ".join(str(elem) for elem in extra_elementsAB)
                    differencesAB.append(f"Hierarchy B has elements at positions: {extra_elementsAB_str} which are not present in Hierarchy A.")
                    differencesAB.append(f"Hierarchy B has {num_extra_elementsAB} more element(s) than Hierarchy A.")
                else:
                    differencesAB.append(f"Hierarchy B has an element at position: {extra_elementsAB[0]} which is not present in Hierarchy A.")
                    differencesAB.append("Hierarchy B has one more element than Hierarchy A.")

            # Check if hierarchy A has fewer elements than hierarchy C
            if len(hierarchy_A[0]) < len(hierarchy_C[0]):
                num_extra_elementsAC = len(hierarchy_C[0]) - len(hierarchy_A[0])
                extra_elementsAC = [i for i in range(len(hierarchy_C[0])) if i >= len(hierarchy_A[0])]
                if len(extra_elementsAC) > 1:
                    extra_elementsAC_str = ", ".join(str(elem) for elem in extra_elementsAC)
                    differencesAB.append(f"Hierarchy C has elements at positions: {extra_elementsAC_str} which are not present in Hierarchy A.")
                    differencesAB.append(f"Hierarchy C has {num_extra_elementsAC} more element(s) than Hierarchy A.")
                else:
                    differencesAB.append(f"Hierarchy C has an element at position: {extra_elementsAC[0]} which is not present in Hierarchy A.")
                    differencesAB.append("Hierarchy C has one more element than Hierarchy A.")


            # Check if hierarchy A has more elements than hierarchy B
            if len(hierarchy_A[0]) > len(hierarchy_B[0]):
                num_missing_elementsAB = len(hierarchy_A[0]) - len(hierarchy_B[0])
                missing_elementsAB = [i for i in range(len(hierarchy_A[0])) if i >= len(hierarchy_B[0])]
                if len(missing_elementsAB) > 1:
                    missing_elements_str = ", ".join(str(elem) for elem in missing_elementsAB)
                    differencesAB.append(f"Hierarchy B is missing elements at positions: {missing_elements_str}.")
                    differencesAB.append(f"Hierarchy B is missing the last {num_missing_elementsAB} element(s).")
                else:
                    differencesAB.append(f"Hierarchy B is missing element at position: {missing_elementsAB[0]}.")
                    differencesAB.append("Hierarchy B is missing the last element.")

            # Check if hierarchy A has more elements than hierarchy C
            if len(hierarchy_A[0]) > len(hierarchy_C[0]):
                num_missing_elementsAC = len(hierarchy_A[0]) - len(hierarchy_C[0])
                missing_elementsAC = [i for i in range(len(hierarchy_A[0])) if i >= len(hierarchy_C[0])]
                if len(missing_elementsAC) > 1:
                    missing_elements_str = ", ".join(str(elem) for elem in missing_elementsAC)
                    differencesAC.append(f"Hierarchy C is missing elements at positions: {missing_elements_str}.")
                    differencesAC.append(f"Hierarchy C is missing the last {num_missing_elementsAC} element(s).")
                else:
                    differencesAC.append(f"Hierarchy C is missing element at position: {missing_elementsAC[0]}.")
                    differencesAC.append("Hierarchy C is missing the last element.")

            # Iterate over the hierarchies and compare each element
            for i in range(min(len(hierarchy_A[0]), len(hierarchy_B[0]))):
                if not np.array_equal(hierarchy_A[0][i], hierarchy_B[0][i]):
                    differencesAB.append(f"Difference at hierarchy[0][{i}]:")
                    differencesAB.append(f"Hierarchy A: {hierarchy_A[0][i]}")
                    differencesAB.append(f"Hierarchy B: {hierarchy_B[0][i]}")
                    differencesAB.append("")  # Add a blank line for separation
             # Iterate over the hierarchies and compare each element
            for i in range(min(len(hierarchy_A[0]), len(hierarchy_C[0]))):
                if not np.array_equal(hierarchy_A[0][i], hierarchy_C[0][i]):
                    differencesAC.append(f"Difference at hierarchy[0][{i}]:")
                    differencesAC.append(f"Hierarchy A: {hierarchy_A[0][i]}")
                    differencesAC.append(f"Hierarchy C: {hierarchy_C[0][i]}")
                    differencesAC.append("")  # Add a blank line for separation

            # Print the differences
            if differencesAB:
                print("Differences between Hierarchy A and Hierarchy B:")
                for difference in differencesAB:
                    print(difference)
            else:
                print("No differences found between Hierarchy A and Hierarchy B.")

            if differencesAC:
                print("Differences between Hierarchy A and Hierarchy C:")
                for difference in differencesAC:
                    print(difference)
            else:
                print("No differences found between Hierarchy A and Hierarchy C.")

           # Variables to store comparison results
            AB_horizontal = AC_horizontal = AB_vertical = AC_vertical = 0
            AB_rotation = AC_rotation = [0, 0, 0]  # For 90, 180, 270 degrees respectively

            # Check if there is any change at all between A and B, and A and C
            AB_change = np.sum(cv2.absdiff(A, B)) == 0
            AC_change = np.sum(cv2.absdiff(A, C)) == 0

            # Check for horizontal reflection similarity
            AB_horizontal = np.sum(cv2.absdiff(cv2.flip(A,1), B)) < tolerance
            AC_horizontal = np.sum(cv2.absdiff(cv2.flip(A,1), C)) < tolerance

            # Check for vertical reflection similarity
            AB_vertical = np.sum(cv2.absdiff(cv2.flip(A, 0), B)) < tolerance
            AC_vertical = np.sum(cv2.absdiff(cv2.flip(A, 0), C)) < tolerance


            # Check for rotation similarity
            if not AB_horizontal and not AB_vertical:
                AB_rotation = [np.sum(cv2.absdiff(B, cv2.rotate(A, rot))) < tolerance for rot in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]]
            if not AC_horizontal and not AC_vertical:
                AC_rotation = [np.sum(cv2.absdiff(C, cv2.rotate(A, rot))) < tolerance for rot in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]]
        
            
            # Create a list to hold the sequence of transformations that would take B to A and C to A
            transformations_to_apply = []
            transformations_difference = []

            transformations_difference.append(f"AB_change: {np.sum(cv2.absdiff(A, B))}")
            transformations_difference.append(f"AC_change: {np.sum(cv2.absdiff(A, C))}")
            transformations_difference.append(f"AB_horizontal: {np.sum(cv2.absdiff(A, cv2.flip(B, 1)))}")
            transformations_difference.append(f"AC_horizontal:  {np.sum(cv2.absdiff(A, cv2.flip(C, 1)))}")
            transformations_difference.append(f"AB_vertical: {np.sum(cv2.absdiff(A, cv2.flip(B, 0)))}")
            transformations_difference.append(f"AC_vertical: {np.sum(cv2.absdiff(A, cv2.flip(C, 0)))}")
            
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
            for i, degree in enumerate([90, 180, 270]):
                if AB_rotation[i] == 1:
                    transformations_to_apply.append(f'Rotation by {degree} degrees between A and B')
                    transformations_to_apply_AB.append(3 + i)
                if AC_rotation[i] == 1:
                    transformations_to_apply.append(f'Rotation by {degree} degrees between A and C')
                    transformations_to_apply_AC.append(3 + i)

            print(image_path)
            print('\n'.join(transformations_difference))
            print('\n'.join(transformations_to_apply))

             # Try to apply the transformations from A->B to C->D and A->C to B->D
            print("===================================")
            for option, D in option_images.items():
                print("Option:", option)
                
                # Initialize counters for successful transformations
                success_count_AB = 0
                success_count_AC = 0

                # Apply each transformation from A to B on image C
                for transformation in transformations_to_apply_AB:
                    transformed_C = apply_transformation(C, transformation)
                    print("Transformation C->D:", transformation, "Transformation difference:", np.sum(cv2.absdiff(transformed_C, D)))

                    if np.sum(cv2.absdiff(transformed_C, D)) < tolerance:
                        success_count_AB += 1
                        print("Transformation C->D:", transformation, "# of transformations analyzed:", success_count_AB)

                # Apply each transformation from A to C on image B
                for transformation in transformations_to_apply_AC:
                    transformed_B = apply_transformation(B, transformation)
                    print("Transformation B->D:", transformation, "Transformation difference:", np.sum(cv2.absdiff(transformed_B, D)))

                    if np.sum(cv2.absdiff(transformed_B, D)) < tolerance:
                        success_count_AC += 1
                        print("Transformation B->D:", transformation, "# of transformations analyzed:", success_count_AC)
                
                max_success_count = max(success_count_AB, success_count_AC)
                if max_success_count > best_success_count:
                    best_option = option
                    best_success_count = max_success_count

                if best_option is not None:
                   print("Answer: ", int(option))
                   print("===================================")
                   #input("Press Enter to continue...")
                   return int(best_option)
            
            for option, D in option_images.items():
                contours_D, hierarchy_D = process_image(D)
                elementsBD = len(hierarchy_B[0]) - len(hierarchy_D[0])
                elementsCD = len(hierarchy_C[0]) - len(hierarchy_D[0])
                print("Option:", option)

                if elementsAB == elementsCD:    
                    print("\\\\\\\\\\\\\\\\\\\\\\\\ CD")
                    success_count_AB += 1
                if elementsAC == elementsBD:        
                    print("\\\\\\\\\\\\\\\\\\\\\\\\ BD")
                    success_count_AC += 1

                max_success_count = max(success_count_AB, success_count_AC)
                if max_success_count > best_success_count:
                    best_option = option
                    best_success_count = max_success_count

                if best_option is not None:
                   print("Answer: ", int(option))
                   print("===================================")
                   #input("Press Enter to continue...")
                   return int(best_option)
                
            for option, D in option_images.items():
                print("Option: ", option)
                edgesD = figure_edges(contours_D, 'D')

                if sum(edgesB) > sum(edgesD):
                    edgesBD = 1
                elif sum(edgesB) < sum(edgesD):
                    edgesBD = -1
                else:
                    edgesBD = 0
                
                if sum(edgesC) > sum(edgesD):
                    edgesCD = 1
                elif sum(edgesC) < sum(edgesD):
                    edgesCD = -1
                else:
                    edgesCD = 0

                if edgesAB == edgesCD:
                    print("EDGES CD")
                    success_count_AB += 1
                if edgesAC == edgesBD:
                    print("EDGES BD")
                    success_count_AB += 1

                max_success_count = max(success_count_AB, success_count_AC)
                if max_success_count > best_success_count:
                    best_option = option
                    best_success_count = max_success_count

                if best_option is not None:
                   print("Answer: ", int(option))
                   print("===================================")
                   #input("Press Enter to continue...")
                   return int(best_option)


            print("No solution")
            print("===================================")
            #input("Press Enter to continue...")


        # If problem is 3x3
        #elif problem.problemType == "3x3":
            #print('This is a 3x3 problem')


        #print("Path: ", image_path, " type: ", problem_type, " visual: ", problem_hasVisual, " verbal: ", problem_hasVerbal)
        return -1