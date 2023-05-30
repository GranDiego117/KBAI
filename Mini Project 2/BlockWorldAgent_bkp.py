class BlockWorldAgent:
    def __init__(self):
        pass
    def solve(self, initial_arrangement, goal_arrangement):
        # determine in which stack the blocks will end
        block_finalStack = {}
        for i, index in enumerate(goal_arrangement):
        	#print("i: ", i, " index: ",index)
            for block in index:
                block_finalStack[block] = i
                #print("block: ", block, initial_arrangement, goal_arrangement)
		
		# Create a copy of the initial arrangement, with each stack represented as a list of blocks from top to bottom
		initial_arrangement2 = []
            for stack in initial_arrangement:
                reversed_stack = list(reversed(stack))
                initial_arrangement2.append(reversed_stack)
                
        #stacks = [list(reversed(stack)) for stack in initial_arrangement]

        # The current positions of each block
        #block_positions = {block: i for i, stack in enumerate(stacks) for block in stack}

        # Store the index of the top block in the goal position in each stack, or len(stack) if no blocks are in the goal position
        #top_goal_blocks = [len(stack) for stack in stacks]

			
                
                
        #Add your code here! Your solve method should receive
		#as input two arrangements of blocks. The arrangements
		#will be given as lists of lists. The first item in each
		#list will be the bottom block on a stack, proceeding
		#upward. For example, this arrangement:
		#
		#[["A", "B", "C"], ["D", "E"]]
		#
		#...represents two stacks of blocks: one with B on top
		#of A and C on top of B, and one with E on top of D.
		#
		#Your goal is to return a list of moves that will convert
		#the initial arrangement into the goal arrangement.
		#Moves should be represented as 2-tuples where the first
		#item in the 2-tuple is what block to move, and the
		#second item is where to put it: either on top of another
		#block or on the table (represented by the string "Table").
		#
		#For example, these moves would represent moving block B
		#from the first stack to the second stack in the example
		#above:
		#
		#("C", "Table")
		#("B", "E")
		#("C", "A")
        pass

def solve(self, initial_arrangement, goal_arrangement):
        # determine in which stack the blocks will end
        block_finalStack = {}
        correct_position = []
        moves = []

        print("Goal: ", goal_arrangement)
        for i, index in enumerate(goal_arrangement):
            #print("i: ", i, " index: ",index)
            for block in index:
                block_finalStack[block] = i
                #print("block: ", block, initial_arrangement, goal_arrangement)
        
        # reverse the stack to work first on the top of each stack
        initial_reversed = []
        for position in initial_arrangement:
            reversed_stack = list(reversed(position))
            initial_reversed.append(reversed_stack)
        print("Original Initial: ",initial_arrangement)
        print("Inverted Initial: ", initial_reversed)

        # Determine the current positions of each block in the reversed stack
        block_positions = {}
        for i, position in enumerate(initial_reversed):
             for block in position:
                  block_positions[block] = i
        print("Block stack: ", block_positions)

        while correct_position != block_finalStack:
            for 

