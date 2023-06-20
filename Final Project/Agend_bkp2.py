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
from skimage.metrics import structural_similarity as ssim
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
    
        def get_pixel_counts(image):
            return {
                'black': np.sum(image == 0),
                'white': np.sum(image == 255)
            }

        def comparison(X,Y,X_name, Y_name):
                XY_horizontal = XY_vertical = 0
                XY_rotation = [0, 0, 0]  # For 90, 180, 270 degrees respectively


                X = cv2.cvtColor(X, cv2.COLOR_BGR2GRAY)
                Y = cv2.cvtColor(Y, cv2.COLOR_BGR2GRAY)

                # Check if there is any change at all between X and Y
                XY_change = ssim(X, Y) >= 0.9
                
                # Check for horizontal reflection similarity
                XY_horizontal = ssim(cv2.flip(X,1), Y) >= 0.9

                # Check for vertical reflection similarity
                XY_vertical = ssim(cv2.flip(X,0), Y) >= 0.9

                # Check for rotation similarity
                if not XY_horizontal and not XY_vertical:
                    [ssim(Y, cv2.rotate(X,rot)) >= 0.9 for rot in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]]

                # Create a list to hold the sequence of transformations that would take Y to X
                transformations_to_apply = []
                transformations_difference = []

                transformations_difference.append(f"XY_change for {X_name} and {Y_name}: {XY_change}")
                transformations_difference.append(f"XY_horizontal for {X_name} and {Y_name}: {XY_horizontal}")
                transformations_difference.append(f"XY_vertical for {X_name} and {Y_name}: {XY_vertical}")

                transformations_to_apply_XY = []

                # Determine the transformations to apply
                if XY_change:
                    transformations_to_apply.append(f'Change not detected between {X_name} and {Y_name}')
                    transformations_to_apply_XY.append(0)
                    
                if XY_horizontal:
                    transformations_to_apply.append(f'Horizontal Reflection between {X_name} and {Y_name}')
                    transformations_to_apply_XY.append(1)
                    

                if XY_vertical:
                    transformations_to_apply.append(f'Vertical Reflection between {X_name} and {Y_name}')
                    transformations_to_apply_XY.append(2)
                    

                for i, degree in enumerate([90, 180, 270]):
                    if XY_rotation[i] == 1:
                        transformations_to_apply.append(f'Rotation by {degree} degrees between {X_name} and {Y_name}')
                        transformations_to_apply_XY.append(3 + i)                        

                print(f"For pair {X_name} and {Y_name}:")
                print('\n'.join(transformations_difference))
                print('\n'.join(transformations_to_apply))
                print("===================================")

                return XY_horizontal, XY_vertical, XY_change, XY_rotation
        
        problem_images = {}
        option_images = {}
        best_option = None
        best_success_count = 0
        tolerance = 800000

        # Tolerance in pixels for image differences
        #tolerance = 500000
        tolerance = 800000

        # Loop over each figure in the problem.
        for name, figure in problem.figures.items():
            # Load the image file.
            image_path = figure.visualFilename
            #image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            image = cv2.imread(image_path,)

            # If the name is a letter, add it to the problem images. 
            if name.isalpha():
                problem_images[name] = image
            # If the name is a number, add it to the options images.
            elif name.isdigit():
                option_images[name] = image

        #if problem is 3x3
        if problem.problemType == "3x3":

            A = problem_images.get('A')
            B = problem_images.get('B')
            C = problem_images.get('C')
            D = problem_images.get('D')
            E = problem_images.get('E')
            F = problem_images.get('F')
            G = problem_images.get('G')
            H = problem_images.get('H')

            A_b_pixels = np.sum(A == 0)
            A_w_pixels = np.sum(A == 255)
            B_b_pixels = np.sum(B == 0)
            B_w_pixels = np.sum(B == 255)
            C_b_pixels = np.sum(C == 0)
            C_w_pixels = np.sum(C == 255)
            D_b_pixels = np.sum(D == 0)
            D_w_pixels = np.sum(D == 255)
            E_b_pixels = np.sum(E == 0)
            E_w_pixels = np.sum(E == 255)
            F_b_pixels = np.sum(F == 0)
            F_w_pixels = np.sum(F == 255)
            G_b_pixels = np.sum(G == 0)
            G_w_pixels = np.sum(G == 255)
            H_b_pixels = np.sum(H == 0)
            H_w_pixels = np.sum(H == 255)

            

            row1 = row2 = row3 = 0
            col1 = col2 = col3 = 0
            diagA = diagB = diagD = 0

            AB_horizontal, AB_vertical, AB_change, AB_rotation = comparison(A,B,'A','B')
            BC_horizontal, BC_vertical, BC_change, BC_rotation = comparison(B, C, 'B', 'C')
            AD_horizontal, AD_vertical, AD_change, AD_rotation = comparison(A, D, 'A', 'D')
            AE_horizontal, AE_vertical, AE_change, AE_rotation = comparison(A, E, 'A', 'E')
            DE_horizontal, DE_vertical, DE_change, DE_rotation = comparison(D, E, 'D', 'E')
            BE_horizontal, BE_vertical, BE_change, BE_rotation = comparison(B, E, 'B', 'E')
            EF_horizontal, EF_vertical, EF_change, EF_rotation = comparison(E, F, 'E', 'F')

            if AB_change or BC_change:
                row1 += 1
            if AD_change:
                col1 += 1
            if AE_change:
                diagA += 1

            print("AB_Change: ", AB_change)
            print("BC_Change: ", BC_change)
            

            A_b_pixels = np.sum(A == 0)
            A_w_pixels = np.sum(A == 255)
            B_b_pixels = np.sum(B == 0)
            B_w_pixels = np.sum(B == 255)
            C_b_pixels = np.sum(C == 0)
            C_w_pixels = np.sum(C == 255)
            D_b_pixels = np.sum(D == 0)
            D_w_pixels = np.sum(D == 255)
            E_b_pixels = np.sum(E == 0)
            E_w_pixels = np.sum(E == 255)
            F_b_pixels = np.sum(F == 0)
            F_w_pixels = np.sum(F == 255)
            G_b_pixels = np.sum(G == 0)
            G_w_pixels = np.sum(G == 255)
            H_b_pixels = np.sum(H == 0)
            H_w_pixels = np.sum(H == 255)

            print("Problem: ", image_path)
            print("A Black Pixel: ", A_b_pixels, " B Black Pixel: ", B_b_pixels, " C Black Pixel: ", C_b_pixels)
            print("D Black Pixel: ", D_b_pixels, " E Black Pixel: ", E_b_pixels, " F Black Pixel: ", F_b_pixels)
            print("G Black Pixel: ", G_b_pixels, " H Black Pixel: ", H_b_pixels)

            print("A White Pixel: ", A_w_pixels, " B White Pixel: ", B_w_pixels, " C White Pixel: ", C_w_pixels)
            print("D White Pixel: ", D_w_pixels, " E White Pixel: ", E_w_pixels, " F White Pixel: ", F_w_pixels)
            print("G White Pixel: ", G_w_pixels, " H White Pixel: ", H_w_pixels)


            contours_A, hierarchy_A = process_image(A)
            contours_B, hierarchy_B = process_image(B)
            contours_C, hierarchy_C = process_image(C)
            contours_D, hierarchy_D = process_image(D)
            contours_E, hierarchy_E = process_image(E)
            contours_F, hierarchy_F = process_image(F)
            contours_G, hierarchy_G = process_image(G)
            contours_H, hierarchy_H = process_image(H)

            # Collect black and white pixel counts in lists for A through H
            black_pixels = [A_b_pixels, B_b_pixels, C_b_pixels, D_b_pixels, E_b_pixels, F_b_pixels, G_b_pixels, H_b_pixels]
            white_pixels = [A_w_pixels, B_w_pixels, C_w_pixels, D_w_pixels, E_w_pixels, F_w_pixels, G_w_pixels, H_w_pixels]

            if AB_change or BC_change:
                row1 += 1
            if AD_change:
                col1 += 1
            if AE_change:
                diagA += 1

            def find_pattern(tolerance=500):
                # Check case 1: A = B = C
                if row1 > 0:
                    return 1
                
                if col1 > 0:
                    return 8
                
                if diagA > 0:
                    return 9

                #if abs(black_pixels[0] - black_pixels[1]) <= tolerance and abs(black_pixels[1] - black_pixels[2]) <= 10 \
                #        and abs(white_pixels[0] - white_pixels[1]) <= tolerance and abs(white_pixels[1] - white_pixels[2]) <= 10:
                #    return 1

                # Check case 2: uniform increase or decrease
                if abs((black_pixels[1] - black_pixels[0]) - (black_pixels[2] - black_pixels[1])) <= tolerance \
                        and abs((white_pixels[1] - white_pixels[0]) - (white_pixels[2] - white_pixels[1])) <= tolerance:
                    return 2

                # Check case 3: doubling/halving (C = 2A)
                if abs(black_pixels[2] - 2 * black_pixels[0]) <= tolerance and abs(white_pixels[2] - 2 * white_pixels[0]) <= tolerance:
                    return 3

                # Check case 4: tripling (C = 3A)
                if abs(black_pixels[2] - 3 * black_pixels[0]) <= tolerance and abs(white_pixels[2] - 3 * white_pixels[0]) <= tolerance:
                    return 4

                # Check case 5: one or two values are significantly different from the others
                mean_black_pixels = sum(black_pixels) / len(black_pixels)
                mean_white_pixels = sum(white_pixels) / len(white_pixels)
                black_outliers = [p for p in black_pixels if abs(p - mean_black_pixels) > tolerance]
                white_outliers = [p for p in white_pixels if abs(p - mean_white_pixels) > tolerance]
                if len(black_outliers) <= 2 and len(white_outliers) <= 2:
                    return 5

                # Check case 6: C = 1.5B, F = 1.5E, etc.
                if abs(black_pixels[2] - 1.5 * black_pixels[1]) <= tolerance and abs(white_pixels[2] - 1.5 * white_pixels[1]) <= tolerance \
                        and abs(black_pixels[5] - 1.5 * black_pixels[4]) <= tolerance and abs(white_pixels[5] - 1.5 * white_pixels[4]) <= tolerance:
                    return 6

                # If none of the above cases matched, return 7
                return 7
            
            pattern = find_pattern()
            print(f'Matched pattern: {pattern}')
                    
            best_option = -1
            
            operation = []

            

            for option, I in option_images.items():
                I_b_pixels = np.sum(I == 0)                
                print("Option:", option)

                if pattern == 1:  # A = B = C
                    print(" H_b_pixels = ", H_b_pixels, I_b_pixels, H_b_pixels - I_b_pixels, option)
                    operation.append(H_b_pixels - I_b_pixels)
                    
                elif pattern == 2:  # Steady increase
                    increase = (black_pixels[1] - black_pixels[0] + black_pixels[2] - black_pixels[1] + black_pixels[5] - black_pixels[4] + black_pixels[4] - black_pixels[3] + black_pixels[7] - black_pixels[6]) / 5
                    print(" H_b_pixels = ", H_b_pixels, increase, I_b_pixels, option, abs(I_b_pixels - (H_b_pixels + increase)))
                    operation.append(abs(I_b_pixels - (H_b_pixels + increase)))
                    
                    
                elif pattern == 3:  # C = 2A
                    print(" H_b_pixels = ", I_b_pixels, G_b_pixels, I_b_pixels/G_b_pixels)
                    operation .append(abs(I_b_pixels / G_b_pixels ) <= 2.1 and abs(I_b_pixels / G_b_pixels ))
        
                else:
                    print("no option")
                
            # Find the minimum operation value and corresponding option
            min_operation = float('inf')
            max_operation = float('-inf')

            if pattern != 3:
                for option, value in zip(option_images.keys(), operation):
                    if value >= 0 and value < min_operation:
                        best_option = option
                        min_operation = value
                print("Best option:", best_option)
                return int(best_option)
            
            if pattern == 3:
                for option, value in zip(option_images.keys(), operation):
                    if value >= 0 and value > max_operation:
                        best_option = option
                        max_operation = value
                print("Best option:", best_option)
                return int(best_option)
                                
            return -1


            

            
            #print('This is a 3x3 problem')

        # If problem is 2x2
        elif problem.problemType == "2x2":
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


        


        #print("Path: ", image_path, " type: ", problem_type, " visual: ", problem_hasVisual, " verbal: ", problem_hasVerbal)
        return -1