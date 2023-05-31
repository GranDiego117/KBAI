import time

class BlockWorldAgent:
    def __init__(self):
        pass

    def solve(self, initial_arrangement, goal_arrangement):
        start_time = time.time()
        # Duplicate the initial_stack_copy into a new one to avoid changing the original configuration
        initial_stack_copy = []
        for stack in initial_arrangement:
            initial_stack_copy.append(stack.copy())
        
        moves = [] # store the movements we'll make
        table = [] # The "Table" where blocks can be placed

        # We will store the blocks into a new set of stacks, so for each stack in the goal_arrangement we'll create a new one.
        temp_stacks = []
        for i, _ in enumerate(goal_arrangement):
            temp_stacks.append([])

        # Print the blocks and stacks to visualize them
        def print_state():
            print("Current arrangement: ", initial_stack_copy)
            print("Table: ", table)
            print("New arrangement: ", temp_stacks)
            print("Goal arrangement: ", goal_arrangement)
            print("Moves: ", moves)
            print("--------------------------------------------------")

        # We'll use block_movement function to move the blocks around
        def block_movement(block, source, destination):
            if source == "Table": 
                table.remove(block) # we remove the block from the table
            else:
                initial_stack_copy[source].remove(block) # we remove the block from the initial stack
            
            if destination == "Table": 
                table.append(block) # we move the block to the table
            else:
                temp_stacks[destination].append(block) #  we move the block to the final "temp_stack"

        # In this first pass, we move all the blocks to either the table or the stack they correspond to if the conditions are met
        for stack in initial_stack_copy:
            while stack:
                block_to_move = stack[-1]
                goal_stack_number = None # the stack in which we want to add our block
               # print("Stack: ", stack, " bloack to move: ", block_to_move)
               # input("Press Enter to continue...")
                    
                # First we check in which stack (in goal_arrangement) is the block we are going to move.
                # essentially, where do we have to move the block to
                for index, goal_stack in enumerate(goal_arrangement):
                    #print("Block to Move: ", block_to_move, "INDEX: ", index, " GOAL_STACK: ", goal_stack)
                    #input("Press Enter to continue...")
                    if block_to_move in goal_stack:
                        goal_stack_number = index
                    #    print("block to move: ", block_to_move, " is in the goal stack ", goal_stack, " in stack ", goal_stack_number)
                    #    input("Press Enter to continue...")
                        break

                #now that we know the stack in which the block should go, we retrieve the position (from bottom to top)
                block_position_in_goal_stack = goal_arrangement[goal_stack_number].index(block_to_move)
                #print("GOAL Stack Number: ", goal_stack_number, "Block: ", block_to_move, " Position in Goal Stack:  ", goal_arrangement[goal_stack_number].index(block_to_move) )
                #input("Press Enter to continue...")

                if block_position_in_goal_stack > 0: # Block to move is not the base in goal
                    #print(" Block is not in base ", block_position_in_goal_stack)
                    #input("Press Enter to continue...")

                    # We retrieve the block in the goal stack that should be below the block we are about to move
                    block_below = goal_arrangement[goal_stack_number][block_position_in_goal_stack - 1]

                    # if the block below is already in the correct stack, we move the block to the stack, otherwise we move it to the table
                    if block_below in temp_stacks[goal_stack_number]:
                        #print("||Block below: ", block_below)
                        #input("Press Enter to continue...")
                        moves.append((block_to_move, block_below))
                        block_movement(block_to_move, initial_stack_copy.index(stack), goal_stack_number)
                    else:
                        #print("||Moves to table: ", block_to_move)
                        #input("Press Enter to continue...")

                        # we check to see if the block is already in the table (i.e., position 0) - if not, we record the movement to the table.
                        if(stack.index(block_to_move) > 0):
                            moves.append((block_to_move, 'Table'))
                        table.append(stack.pop())
                
                # ELSE - the block is the base of one of the stacks, so we check whether the block is already on the table
                else:
                    if(stack.index(block_to_move) > 0):
                        moves.append((block_to_move, 'Table'))
                    block_movement(block_to_move, initial_stack_copy.index(stack), goal_stack_number)
                    #print("Block ", block_to_move, " is currently in ", initial_stack_copy.index(stack), " and moving to: ", goal_stack_number)
                    #input("Press Enter to continue...")

        # in this second pass, we move all the blocks from the table to the right stack in the right order
        for goal_stack_number, goal_stack in enumerate(goal_arrangement):
            #print("Goal Stack Index: ", goal_stack_number, " Goal Stack: ", goal_stack, " enumarate goal stack: ", enumerate(goal_arrangement))
            #input("Press Enter to continue...")

            for i in range(len(goal_stack)):
                block = goal_stack[i]
                #print(" Block: ", block, " goal_stack: ", goal_stack, " i: ", i, " table: ", table)
                #input("Press Enter to continue...")

                if block in table:
                    if i > 0 and temp_stacks[goal_stack_number][-1] != goal_stack[i - 1]:
                        #print("|IF i>0... new arrangement: ", temp_stacks, " goal_stack_number ", goal_stack_number, " goal stack ", goal_stack)
                        #input("Press Enter to continue...")
                        continue

                    if i > 0:
                        moves.append((block, temp_stacks[goal_stack_number][-1])) # reference to the block underneath in new arrangement
                        #print("|IF I>0... New Arrangement: ", temp_stacks, " Block underneath: ", temp_stacks[goal_stack_number][-1], " Moves: ", moves)
                        #input("Press Enter to continue...")
                    else:
                        moves.append((block, goal_stack[0]))
                        #print("| ELSE ... Moves: ", goal_stack)
                        #input("Press Enter to continue...")

                    block_movement(block, "Table", goal_stack_number)
                    #print_state()
        elapsed_time = time.time() - start_time
        print(" time: ", elapsed_time)
        return moves