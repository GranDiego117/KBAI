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
from PIL import Image
import numpy as np

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

            if name.isalpha():
                problem_images[name] = image
            elif name.isdigit():
                option_images[name] = image
            
            #print(f"Figure name: {name}, visualFilename: {figure.visualFilename}, problemType: {problem.problemType}")
        
        problem_arrays = [np.array(image) for image in problem_images.values()]
        are_problem_images_identical = all(np.array_equal(problem_arrays[0], prompt_array) for prompt_array in problem_arrays)

        print(f"Are all prompt images identical? {are_problem_images_identical}")

        if are_problem_images_identical:
            for option_name, option_image in option_images.items():
                if np.array_equal(problem_arrays[0], np.array(option_image)):
                    print(f"Option {option_name} is identical to the problem images.")
                    return int(option_name)


        #print("Path: ", image_path, " type: ", problem_type, " visual: ", problem_hasVisual, " verbal: ", problem_hasVerbal)
        return -1