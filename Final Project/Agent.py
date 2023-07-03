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
import numpy as np
import cv2
import time



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
        start_time = time.time()

        def process_image(image):
            # Convert the image to grayscale and binary
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            # Find contours and hierarchy
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            return contours, hierarchy
        
        def apply_transformation(image, transformation):
            if transformation == 0:  # change
                #print("|| Transformation = Change")
                return image
            elif transformation == 1:  # horizontal
                #print("|| Transformation = Horizontal")
                image = cv2.flip(image, 1)
            elif transformation == 2:  # vertical
                #print("|| Transformation = Vertical")
                image = cv2.flip(image, 0)
            elif transformation == 3:  # rotation_90
                #print("|| Transformation = rotation 90")
                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE )
            elif transformation == 4:  # rotation_180
                #print("|| Transformation = rotation 180")
                image = cv2.rotate(image, cv2.ROTATE_180)
            elif transformation == 5:  # rotation_270
                #print("|| Transformation = rotation 270")
                image = cv2.rotate(image,  cv2.ROTATE_90_COUNTERCLOCKWISE) 
            return image
        
        # Function to detect and #print the number of edges for each figure in an image
        def figure_edges(contours, image_name):
            edges_count = []
            #print(f"Figures in {image_name}:")
            for i, contour in enumerate(contours):
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                num_edges = len(approx)
                #print(f"Figure {i+1}: {num_edges} edges")
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
        tolerance = 800000

        # Loop over each figure in the problem.
        for name, figure in problem.figures.items():
            # Load the image file.
            image_path = figure.visualFilename
            #image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            image = cv2.imread(image_path, )

            # If the name is a letter, add it to the problem images. 
            if name.isalpha():
                problem_images[name] = image
            # If the name is a number, add it to the options images.
            elif name.isdigit():
                option_images[name] = image

        print(" PROBLEM: ",image_path)

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

            # Initialize a dictionary to store the report for each image
            image_info = {}

            def figure_matches(image1, image2, tolerance):
                for figure1 in image1['total_pixels']:
                    for figure2 in image2['total_pixels']:
                        if abs(figure1 - figure2) <= tolerance:
                            return True
                return False
            
            def similar_pixel_counts(pixels1, pixels2, tolerance):
                if len(pixels1) != len(pixels2):
                    return False
                return all(abs(p1 - p2) <= tolerance for p1, p2 in zip(sorted(pixels1), sorted(pixels2)))


            # For each image in the dictionary
            for name, img in problem_images.items():
                # Ensure image is grayscale
                if len(img.shape) > 2:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)

                # Find connected components in the binary image
                num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(img_bin, connectivity=8)
                            
                # Store figure info for the current option
                figures_info = {"figures_count": num_labels - 1, "total_pixels": [], "binary_img": img_bin}

                # Process each figure (skip 0 because it is the background)
                for i in range(1, num_labels):
                    figure_pixels = np.sum(labels == i)
                    figures_info["total_pixels"].append(figure_pixels)

                image_info[name] = figures_info  
            

            #print("=========================")
            #print(image_path)

            # Initialize the result dictionary
            results = {}

            # Perform operations on binary versions of images
            bitwise_and_AB = cv2.bitwise_and(image_info['A']['binary_img'], image_info['B']['binary_img'])
            bitwise_or_AB = cv2.bitwise_or(image_info['A']['binary_img'], image_info['B']['binary_img'])
            bitwise_xor_AB = cv2.bitwise_xor(image_info['A']['binary_img'], image_info['B']['binary_img'])
        

            bitwise_and_AC = cv2.bitwise_and(image_info['A']['binary_img'], image_info['C']['binary_img'])
            bitwise_or_AC = cv2.bitwise_or(image_info['A']['binary_img'], image_info['C']['binary_img'])
            bitwise_xor_AC = cv2.bitwise_xor(image_info['A']['binary_img'], image_info['C']['binary_img'])

            bitwise_and_GH = cv2.bitwise_and(image_info['G']['binary_img'], image_info['H']['binary_img'])
            bitwise_or_GH = cv2.bitwise_or(image_info['G']['binary_img'], image_info['H']['binary_img'])
            bitwise_xor_GH = cv2.bitwise_xor(image_info['G']['binary_img'], image_info['H']['binary_img'])

            bitwise_not_xor_GH = cv2.bitwise_not(cv2.bitwise_xor(image_info['G']['binary_img'], image_info['H']['binary_img']))
            bitwise_not_xor_AB = cv2.bitwise_not(cv2.bitwise_xor(image_info['A']['binary_img'], image_info['B']['binary_img']))


            # Find connected components in the binary image for each bitwise image and store the results
            for bitwise_image, name in zip([bitwise_and_AB, bitwise_or_AB, bitwise_xor_AB, 
                                            bitwise_and_AC, bitwise_or_AC, bitwise_xor_AC, 
                                            bitwise_and_GH, bitwise_or_GH, bitwise_xor_GH, 
                                            bitwise_not_xor_GH, bitwise_not_xor_AB], 
                                        ['and_AB', 'or_AB', 'xor_AB', 
                                        'and_AC', 'or_AC', 'xor_AC', 
                                        'and_GH', 'or_GH', 'xor_GH', 
                                        'not_xor_GH', 'not_xor_AB']):
                num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(bitwise_image, connectivity=8)
                figures_info = {"figures_count": num_labels - 1, "total_pixels": []}

                # Process each figure (skip 0 because it is the background)
                for i in range(1, num_labels):
                    #print("||| i", i)
                    if 'not_xor' in name:
                        
                        figure_pixels = np.sum(labels == i)
                        if figure_pixels < 10000: 
                            figures_info["total_pixels"].append(figure_pixels)
                            #print(" Figure Pixels nor xor: ", figure_pixels)
                        
                    else:
                        figure_pixels = np.sum(labels == i)
                        figures_info["total_pixels"].append(figure_pixels)
                        #print(" Figure Pixels: ", figure_pixels)
                #input("Press Enter to continue...")

                image_info[name] = figures_info

            logic_threshold = 200
            
            ABC_same = image_info['A']['figures_count'] == image_info['B']['figures_count'] == image_info['C']['figures_count'] and \
                        similar_pixel_counts(image_info['A']['total_pixels'], image_info['B']['total_pixels'], logic_threshold)

            results['ABC'] = ABC_same

            AND_AB_same_C = similar_pixel_counts(image_info['and_AB']['total_pixels'], image_info['C']['total_pixels'], logic_threshold)
                            
            OR_AB_same_C = similar_pixel_counts(image_info['or_AB']['total_pixels'], image_info['C']['total_pixels'], logic_threshold)

            xor_pixels = image_info['xor_AB']['total_pixels']
            c_pixels = image_info['C']['total_pixels']

            while len(xor_pixels) < len(c_pixels):
                xor_pixels.append(0)
            while len(c_pixels) < len(xor_pixels):
                c_pixels.append(0)

            XOR_AB_same_C = all(abs(p1 - p2) for p1, p2 in zip(image_info['xor_AB']['total_pixels'], image_info['C']['total_pixels']))
            
            print(all(abs(p1 - p2) for p1, p2 in zip(image_info['xor_AB']['total_pixels'], image_info['C']['total_pixels'])))
            for p1, p2 in zip(image_info['xor_AB']['total_pixels'], image_info['C']['total_pixels']):
                print(" P1: ", p1)
                print(" P2: ", p2)

            
            print(" XOR AB - FigureS: ", image_info['xor_AB']['figures_count'], " Pixels: ", image_info['xor_AB']['total_pixels'], " XOR_AB flag: ", XOR_AB_same_C)
            print(" C- FigureS: ", image_info['C']['figures_count'], " Pixels: ", image_info['C']['total_pixels'])
            print(" Not XOR pixels: ", image_info['not_xor_AB']['total_pixels'])

            results['AND_AB_same_C'] = AND_AB_same_C
            results['OR_AB_same_C'] = OR_AB_same_C
            results['XOR_AB_same_C'] = XOR_AB_same_C

            AND_AC_same_B = similar_pixel_counts(image_info['and_AC']['total_pixels'], image_info['B']['total_pixels'], logic_threshold)

            OR_AC_same_B = similar_pixel_counts(image_info['or_AC']['total_pixels'], image_info['B']['total_pixels'], logic_threshold)

            xorab_pixels = image_info['xor_AC']['total_pixels']
            b_pixels = image_info['B']['total_pixels']

            while len(xorab_pixels) < len(b_pixels):
                xorab_pixels.append(0)
            while len(b_pixels) < len(xorab_pixels):
                b_pixels.append(0)

            XOR_AC_same_B = all(abs(p1 - p2) == 0 for p1, p2 in zip(image_info['xor_AC']['total_pixels'], image_info['B']['total_pixels']))
            
            print(all(abs(p1 - p2) for p1, p2 in zip(image_info['xor_AC']['total_pixels'], image_info['B']['total_pixels'])))
            for p1, p2 in zip(image_info['xor_AC']['total_pixels'], image_info['B']['total_pixels']):
                print(" P1: ", p1)
                print(" P2: ", p2)
            print(" XOR AC - FigureS: ", image_info['xor_AC']['figures_count'], " Pixels: ", image_info['xor_AC']['total_pixels'], " XOR_AC flag: ", XOR_AC_same_B)
            print(" B- FigureS: ", image_info['B']['figures_count'], " Pixels: ", image_info['B']['total_pixels'])


            results['AND_AC_same_B'] = AND_AC_same_B
            results['OR_AC_same_B'] = OR_AC_same_B
            results['XOR_AC_same_B'] = XOR_AC_same_B


            #cv2.imshow('XOR_AC', bitwise_xor_AC)
            #cv2.imshow('XOR_AB', bitwise_xor_AB)
            #cv2.imshow('NOT_XOR_GH', bitwise_not_xor_GH)
            #cv2.imshow('OR_AC_B', bitwise_or_AC)
            #cv2.imshow('C', C)
            #cv2.imshow('B', B)
            #cv2.imshow('A', A)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            
            
            # 1. Compare A, B, and C
            ABC_same = image_info['A']['figures_count'] == image_info['B']['figures_count'] == image_info['C']['figures_count'] and \
                        similar_pixel_counts(image_info['A']['total_pixels'], image_info['B']['total_pixels'], 100)

            results['ABC'] = ABC_same

            # 2. Compare A, D, and G
            ADG_same = image_info['A']['figures_count'] == image_info['D']['figures_count'] == image_info['G']['figures_count'] and \
                        similar_pixel_counts(image_info['A']['total_pixels'], image_info['D']['total_pixels'], 100)

            results['ADG'] = ADG_same

            # 3. Compare A and E, and B and F
            A_E_same = image_info['A']['figures_count'] == image_info['E']['figures_count'] and \
                        similar_pixel_counts(image_info['A']['total_pixels'], image_info['E']['total_pixels'], 100)

            B_F_same = image_info['B']['figures_count'] == image_info['F']['figures_count'] and \
                        similar_pixel_counts(image_info['B']['total_pixels'], image_info['F']['total_pixels'], 100)

            results['A_E_B_F'] = A_E_same and B_F_same

            # 4. Check if any figure in A matches any figure in B
            results['A_B_figure_match'] = figure_matches(image_info['A'], image_info['B'], 100)

            # 5. Check if any figure in A matches any figure in C
            results['A_C_figure_match'] = figure_matches(image_info['A'], image_info['C'], 100)

            # 6. Check if any figure in A matches any figure in D
            results['A_D_figure_match'] = figure_matches(image_info['A'], image_info['D'], 100)

            # 7. Check if any figure in A matches any figure in G
            results['A_G_figure_match'] = figure_matches(image_info['A'], image_info['G'], 100)

            # 8. Check the increase in pixels from A to B and B to C
            increase_rate_A_B = [p2 / p1 if p1 != 0 else float('inf') for p1, p2 in zip(image_info['A']['total_pixels'], image_info['B']['total_pixels'])]
            increase_rate_B_C = [p2 / p1 if p1 != 0 else float('inf') for p1, p2 in zip(image_info['B']['total_pixels'], image_info['C']['total_pixels'])]
            increase_rate_G_H = [p2 / p1 if p1 != 0 else float('inf') for p1, p2 in zip(image_info['G']['total_pixels'], image_info['H']['total_pixels'])]
            avg_increase_rate_A_C = (sum(increase_rate_A_B) + sum(increase_rate_B_C))/2


            results['increase_rate_A_B'] = increase_rate_A_B
            results['increase_rate_B_C'] = increase_rate_B_C
            results['increase_rate_G_H'] = increase_rate_G_H
            results['increase_rate_avg_B_C'] = avg_increase_rate_A_C
            

            # Calculate the pixel change from G to H
            pixel_change_G_H = sum(image_info['H']['total_pixels']) - sum(image_info['G']['total_pixels'])
            if pixel_change_G_H > 0:
                pixel_change_G_H = 1
            elif pixel_change_G_H < 0:
                pixel_change_G_H = -1
            else:
                pixel_change_G_H = 0

            results['pixel_change_G_H'] = pixel_change_G_H

            figure_change_G_H = image_info['H']['figures_count'] - image_info['G']['figures_count']
            if figure_change_G_H > 0:
                figure_change_G_H = 1
            elif figure_change_G_H < 0:
                figure_change_G_H = -1
            else:
                figure_change_G_H = 0


            # #print the results
            for key, value in results.items():
                print("||", key, value)


            for option_name, option_img in option_images.items():
                print("Option Name: ", option_name)
                # Ensure image is grayscale
                if len(option_img.shape) > 2:  
                    option_img = cv2.cvtColor(option_img, cv2.COLOR_BGR2GRAY)

                _, option_img_bin = cv2.threshold(option_img, 128, 255, cv2.THRESH_BINARY_INV)

                # Resize the option image to match 'A'
                option_img_bin = cv2.resize(option_img_bin, (problem_images['A'].shape[1], problem_images['A'].shape[0]))

                # Find connected components in the binary image
                num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(option_img_bin, connectivity=8)

                option_info = {
                    "figures_count": num_labels - 1,  # Subtract 1 for the background label
                    "total_pixels": stats[1:, cv2.CC_STAT_AREA].tolist(),  # Ignore the background label
                    "binary_img": option_img_bin
                }

                if OR_AB_same_C:
                    if (image_info['or_GH']['figures_count'] == option_info['figures_count'] and \
                            similar_pixel_counts(image_info['or_GH']['total_pixels'], option_info['total_pixels'], logic_threshold)):
                        print(" GH or Option same")
                        elapsed_time = time.time() - start_time
                        print(" time: ", elapsed_time)
                        return int(option_name)

                if XOR_AB_same_C:
                    print(" XOR GH: ", image_info['xor_GH']['total_pixels'], " Option info: ", option_info['total_pixels'])
                    if (similar_pixel_counts(image_info['xor_GH']['total_pixels'], option_info['total_pixels'], 350)):
                        print(" GH XOR Option same")
                        elapsed_time = time.time() - start_time
                        print(" time: ", elapsed_time)
                        return int(option_name)

                if AND_AB_same_C:
                    if (image_info['and_GH']['figures_count'] == option_info['figures_count'] and \
                            similar_pixel_counts(image_info['and_GH']['total_pixels'], option_info['total_pixels'], logic_threshold)):
                        print(" GH and Option same")
                        elapsed_time = time.time() - start_time
                        print(" time: ", elapsed_time)
                        return int(option_name)
                    
                    
                if XOR_AC_same_B:
                    #not_xor = image_info['not_xor_GH']['total_pixels']
                    #option_pixels = option_info['total_pixels']

                    #while len(not_xor) < len(option_pixels):
                    #    xorab_pixels.append(0)
                    #while len(option_pixels) < len(not_xor):
                    #    option_pixels.append(0)
                    print("Enter")
                    print(all(abs(p1 - p2) for p1, p2 in zip(image_info['not_xor_GH']['total_pixels'], option_info['total_pixels'])))
                    for p1, p2 in zip(image_info['not_xor_GH']['total_pixels'], option_info['total_pixels']):
                        print(" P1: ", p1)
                        print(" P2: ", p2)
                    print(" Not XOR GH - FigureS: ", image_info['not_xor_GH']['figures_count'], " Pixels: ", image_info['not_xor_GH']['total_pixels'])
                    print(" Option - FigureS: ", option_info['figures_count'], " Pixels: ", option_info['total_pixels'])

                    if (similar_pixel_counts(image_info['not_xor_GH']['total_pixels'], option_info['total_pixels'], logic_threshold)):
                        print(" GH NOT XOR Option same")
                        elapsed_time = time.time() - start_time
                        print(" time: ", elapsed_time)
                        return int(option_name)
                


            

            for option_name, option_img in option_images.items():
                #print("Option Name: ", option_name)
                # Ensure image is grayscale
                if len(option_img.shape) > 2:  
                    option_img = cv2.cvtColor(option_img, cv2.COLOR_BGR2GRAY)

                _, option_img_bin = cv2.threshold(option_img, 128, 255, cv2.THRESH_BINARY_INV)

                # Find connected components in the binary image
                num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(option_img_bin, connectivity=8)

                option_info = {
                    "figures_count": num_labels - 1,  # Subtract 1 for the background label
                    "total_pixels": stats[1:, cv2.CC_STAT_AREA].tolist()  # Ignore the background label
                }

                # Compare the option image with the corresponding image based on the flags
                #print("|||", option_info)
                #print("||| H ", image_info['H']['total_pixels'])
                #print("||| F ", image_info['F']['total_pixels'])
                #print("||| E ", image_info['E']['total_pixels'])
                if results['ABC'] and \
                    option_info["figures_count"] == image_info['H']['figures_count'] and \
                    similar_pixel_counts(option_info['total_pixels'], image_info['H']['total_pixels'], 100):
                    elapsed_time = time.time() - start_time
                    print(" time: ", elapsed_time)
                    return int(option_name)

                if results['ADG'] and \
                    option_info["figures_count"] == image_info['F']['figures_count'] and \
                    similar_pixel_counts(option_info['total_pixels'], image_info['F']['total_pixels'], 100):
                    elapsed_time = time.time() - start_time
                    print(" time: ", elapsed_time)
                    return int(option_name)

                if results['A_E_B_F'] and \
                    option_info["figures_count"] == image_info['E']['figures_count'] and \
                    similar_pixel_counts(option_info['total_pixels'], image_info['E']['total_pixels'], 100):
                    elapsed_time = time.time() - start_time
                    print(" time: ", elapsed_time)
                    return int(option_name)



            for option_name, option_img in option_images.items():
                #print("Option Name: ", option_name)
                # Ensure image is grayscale
                if len(option_img.shape) > 2:  # i.e. has more than one channel
                    option_img = cv2.cvtColor(option_img, cv2.COLOR_BGR2GRAY)

                _, option_img_bin = cv2.threshold(option_img, 128, 255, cv2.THRESH_BINARY_INV)

                num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(option_img_bin, connectivity=8)

                option_info = {
                    "figures_count": num_labels - 1,  # Subtract 1 for the background label
                    "total_pixels": stats[1:, cv2.CC_STAT_AREA].tolist()  # Ignore the background label
                }

                #print(" PIXELS: ", sum(image_info['H']['total_pixels']), sum(option_info['total_pixels']))
                pixel_change_option_H =  sum(option_info['total_pixels']) - sum(image_info['H']['total_pixels'])
                if pixel_change_option_H > 0:
                    pixel_change_option_H = 1
                elif pixel_change_option_H < 0:
                    pixel_change_option_H = -1
                else:
                    pixel_change_option_H = 0

                figure_change_option_H = option_info['figures_count'] - image_info['H']['figures_count']
                if figure_change_option_H > 0:
                    figure_change_option_H = 1
                elif figure_change_option_H < 0:
                    figure_change_option_H = -1
                else:
                    figure_change_option_H = 0

                #print(" H INFO: ", image_info['H'])
                #print(" OPTION INFO: ", option_info)
                #print(" Pixel Change: ", pixel_change_G_H, pixel_change_option_H, pixel_change_option_H * pixel_change_G_H)
                

                # 1. if there's a match AB, AC and AD and AG -> then option should have a figure match G,H and C,F
                if results['A_B_figure_match'] and results['A_C_figure_match'] and results['A_D_figure_match'] and results['A_G_figure_match']:
                    if figure_matches(option_info, image_info['G'], 100) and \
                    figure_matches(option_info, image_info['H'], 100) and \
                    figure_matches(option_info, image_info['C'], 100) and \
                    figure_matches(option_info, image_info['F'], 100) and \
                    pixel_change_G_H == pixel_change_option_H and \
                    figure_change_G_H == figure_change_option_H:
                            #print(f'Option {option_name} matches G, H, C or F for the A_B_C_D_G_figure_match flags')
                            elapsed_time = time.time() - start_time
                            print(" time: ", elapsed_time)
                            return int(option_name)

                # 2. if there's a match AC and AG -> then option should have a figure match G and C
                if results['A_C_figure_match'] and results['A_G_figure_match']:
                    if figure_matches(option_info, image_info['G'], 100) and \
                    figure_matches(option_info, image_info['C'], 100) and \
                    pixel_change_G_H == pixel_change_option_H and \
                    figure_change_G_H == figure_change_option_H:
                        #print(f'Option {option_name} matches G or C for the A_C_G_figure_match flags')
                        elapsed_time = time.time() - start_time
                        print(" time: ", elapsed_time)
                        return int(option_name)

                if results['ABC'] and \
                    option_info["figures_count"] == image_info['H']['figures_count'] and \
                    similar_pixel_counts(option_info['total_pixels'], image_info['H']['total_pixels'], 100) and \
                    pixel_change_G_H == pixel_change_option_H and \
                    figure_change_G_H == figure_change_option_H:
                        #print(f'Option {option_name} matches H for the ABC flag')
                        elapsed_time = time.time() - start_time
                        print(" time: ", elapsed_time)
                        return int(option_name)
                
                if results['ADG'] and \
                    option_info["figures_count"] == image_info['F']['figures_count'] and \
                    similar_pixel_counts(option_info['total_pixels'], image_info['F']['total_pixels'], 100) and \
                    pixel_change_G_H == pixel_change_option_H and \
                    figure_change_G_H == figure_change_option_H:
                        #print(f'Option {option_name} matches F for the ADG flag')
                        elapsed_time = time.time() - start_time
                        print(" time: ", elapsed_time)
                        return int(option_name)

                if results['A_E_B_F'] and \
                    option_info["figures_count"] == image_info['E']['figures_count'] and \
                    similar_pixel_counts(option_info['total_pixels'], image_info['E']['total_pixels'], 100) and \
                    pixel_change_G_H == pixel_change_option_H and \
                    figure_change_G_H == figure_change_option_H:
                        #print(f'Option {option_name} matches E for the A_E_B_F flag')
                        elapsed_time = time.time() - start_time
                        print(" time: ", elapsed_time)
                        return int(option_name)
                
                #print("///////////////////", results['A_C_figure_match'], results['A_G_figure_match'])
                if results['A_C_figure_match'] and results['A_G_figure_match'] and\
                    option_info["figures_count"] == image_info['A']['figures_count'] and \
                    similar_pixel_counts(option_info['total_pixels'], image_info['A']['total_pixels'], 100):
                        #print(f'Option {option_name} matches A for the A_C and AG_G flag')
                        elapsed_time = time.time() - start_time
                        print(" time: ", elapsed_time)
                        return int(option_name)
                

            option_increase_rates = {}

            for option_name, option_img in option_images.items():
                #print("Option Name: ", option_name)
                # Ensure image is grayscale
                if len(option_img.shape) > 2:  
                    option_img = cv2.cvtColor(option_img, cv2.COLOR_BGR2GRAY)

                _, option_img_bin = cv2.threshold(option_img, 128, 255, cv2.THRESH_BINARY_INV)

                # Find connected components in the binary image
                num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(option_img_bin, connectivity=8)

                option_info = {
                    "figures_count": num_labels - 1,  # Subtract 1 for the background label
                    "total_pixels": stats[1:, cv2.CC_STAT_AREA].tolist()  # Ignore the background label
                }

                increase_rate_H_Option = [p2 / p1 if p1 != 0 else float('inf') for p1, p2 in zip(image_info['H']['total_pixels'], option_info['total_pixels'])]
                #print("Increase H_Opt: ", increase_rate_H_Option )

                diff = np.abs(np.mean(increase_rate_H_Option) - np.mean(increase_rate_G_H))

                option_increase_rates[option_name] = (increase_rate_H_Option, diff)
            
            # Find the option with the closest increase rate
            best_option = min(option_increase_rates, key=lambda x: option_increase_rates[x][1])
            #print("BEST OPTION: ", best_option)
            elapsed_time = time.time() - start_time
            print(" time: ", elapsed_time)
            return int(best_option)

           # #print("========================================")            
           # input("Press Enter to continue...")
                
            
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

            #print("Hierarchy A: ", hierarchy_A, "Hierarchy B: ", hierarchy_B)

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

            # #print the differences
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

            #print(image_path)
            #print('\n'.join(transformations_difference))
            #print('\n'.join(transformations_to_apply))

             # Try to apply the transformations from A->B to C->D and A->C to B->D
            #print("===================================")
            for option, D in option_images.items():
                #print("Option:", option)
                
                # Initialize counters for successful transformations
                success_count_AB = 0
                success_count_AC = 0

                # Apply each transformation from A to B on image C
                for transformation in transformations_to_apply_AB:
                    transformed_C = apply_transformation(C, transformation)
                    #print("Transformation C->D:", transformation, "Transformation difference:", np.sum(cv2.absdiff(transformed_C, D)))

                    if np.sum(cv2.absdiff(transformed_C, D)) < tolerance:
                        success_count_AB += 1
                        #print("Transformation C->D:", transformation, "# of transformations analyzed:", success_count_AB)

                # Apply each transformation from A to C on image B
                for transformation in transformations_to_apply_AC:
                    transformed_B = apply_transformation(B, transformation)
                    #print("Transformation B->D:", transformation, "Transformation difference:", np.sum(cv2.absdiff(transformed_B, D)))

                    if np.sum(cv2.absdiff(transformed_B, D)) < tolerance:
                        success_count_AC += 1
                        #print("Transformation B->D:", transformation, "# of transformations analyzed:", success_count_AC)
                
                max_success_count = max(success_count_AB, success_count_AC)
                if max_success_count > best_success_count:
                    best_option = option
                    best_success_count = max_success_count

                if best_option is not None:
                   #print("Answer: ", int(option))
                   #print("===================================")
                   #input("Press Enter to continue...")
                   return int(best_option)
            
            for option, D in option_images.items():
                contours_D, hierarchy_D = process_image(D)
                elementsBD = len(hierarchy_B[0]) - len(hierarchy_D[0])
                elementsCD = len(hierarchy_C[0]) - len(hierarchy_D[0])
                #print("Option:", option)

                if elementsAB == elementsCD:    
                    #print("\\\\\\\\\\\\\\\\\\\\\\\\ CD")
                    success_count_AB += 1
                if elementsAC == elementsBD:        
                    #print("\\\\\\\\\\\\\\\\\\\\\\\\ BD")
                    success_count_AC += 1

                max_success_count = max(success_count_AB, success_count_AC)
                if max_success_count > best_success_count:
                    best_option = option
                    best_success_count = max_success_count

                if best_option is not None:
                   #print("Answer: ", int(option))
                   #print("===================================")
                   #input("Press Enter to continue...")
                   return int(best_option)
                
            for option, D in option_images.items():
                #print("Option: ", option)
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
                    #print("EDGES CD")
                    success_count_AB += 1
                if edgesAC == edgesBD:
                    #print("EDGES BD")
                    success_count_AB += 1

                max_success_count = max(success_count_AB, success_count_AC)
                if max_success_count > best_success_count:
                    best_option = option
                    best_success_count = max_success_count

                if best_option is not None:
                   #print("Answer: ", int(option))
                   #print("===================================")
                   #input("Press Enter to continue...")
                   return int(best_option)


            #print("No solution")
            #print("===================================")
            #input("Press Enter to continue...")


        ##print("Path: ", image_path, " type: ", problem_type, " visual: ", problem_hasVisual, " verbal: ", problem_hasVerbal)
        return -1