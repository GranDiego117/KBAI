class BlockWorldAgent:
    def __init__(self):
        pass

    def solve(self, initial_arrangement, goal_arrangement):
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

        # We'll use move_block function to move the blocks around
        def move_block(block, source, destination):
            if source == "Table": 
                table.remove(block) # ELSE we remove the block from the table
            else:
                initial_stack_copy[source].remove(block) # If the block is NOT on the table, we'll remove them from the initial stack
            
            if destination != "Table": # If the bloock is not going to the table, we move it to the final "temp_stack"
                temp_stacks[destination].append(block)
            else:
                table.append(block) # ELSE we move the block to the table

        for stack in initial_stack_copy:
            while stack:
                block_to_move = stack[-1]
                goal_stack_index = None
               # print("Stack: ", stack, " bloack to move: ", block_to_move)
               # input("Press Enter to continue...")
                    
                # First we check in which stack (in goal_arrangement) is the block we are going to move.
                # essentially, where do we have to move the block to
                for index, goal_stack in enumerate(goal_arrangement):
                    #print("Block to Move: ", block_to_move, "INDEX: ", index, " GOAL_STACK: ", goal_stack)
                    #input("Press Enter to continue...")
                    if block_to_move in goal_stack:
                        goal_stack_index = index
                    #    print("block to move: ", block_to_move, " is in the goal stack ", goal_stack, " in stack ", goal_stack_index)
                    #    input("Press Enter to continue...")
                        break
                
                # Assuming that we know the destination of the 
                if goal_stack_index is not None:
                    block_position_in_goal_stack = goal_arrangement[goal_stack_index].index(block_to_move)
                    #print("Block Position in Goal Stack:  ", goal_arrangement[goal_stack_index].index(block_to_move) )
                    #input("Press Enter to continue...")
                    if block_position_in_goal_stack > 0: # Block to move is not the base in goal
                        #print(" Block is not in base ", block_position_in_goal_stack)
                        #input("Press Enter to continue...")
                        block_below = goal_arrangement[goal_stack_index][block_position_in_goal_stack - 1]
                        if block_below in temp_stacks[goal_stack_index]:
                            #print("||Block below: ", block_below)
                            #input("Press Enter to continue...")
                            moves.append((block_to_move, block_below))
                            move_block(block_to_move, initial_stack_copy.index(stack), goal_stack_index)
                        else:
                            #print("||Moves to table: ", block_to_move)
                            #input("Press Enter to continue...")
                            if(stack.index(block_to_move) > 0):
                                moves.append((block_to_move, 'Table'))
                            table.append(stack.pop())
                    else:
                        if(stack.index(block_to_move) > 0):
                            moves.append((block_to_move, 'Table'))
                        move_block(block_to_move, initial_stack_copy.index(stack), goal_stack_index)
                        #print("Block ", block_to_move, " is currently in ", initial_stack_copy.index(stack), " and moving to: ", goal_stack_index)
                        #input("Press Enter to continue...")
                else:
                    #print(" Else - ", block_to_move, " to table ")
                    #input("Press Enter to continue...")
                    moves.append((block_to_move, 'Table'))
                    table.append(stack.pop())
                print_state()

        for goal_stack_index, goal_stack in enumerate(goal_arrangement):
            #print("Goal Stack Index: ", goal_stack_index, " Goal Stack: ", goal_stack, " enumarate goal stack: ", enumerate(goal_arrangement))
            #input("Press Enter to continue...")
            for i in range(len(goal_stack)):
                block = goal_stack[i]
                #print(" Block: ", block, " goal_stack: ", goal_stack, " i: ", i, " table: ", table)
                #input("Press Enter to continue...")

                if block in table:
                    if i > 0 and temp_stacks[goal_stack_index][-1] != goal_stack[i - 1]:
                       # print("|IF i>0... new arrangement: ", temp_stacks, " goal_stack_index ", goal_stack_index, " goal stack ", goal_stack)
                        #input("Press Enter to continue...")
                        continue

                    if i > 0:
                        moves.append((block, temp_stacks[goal_stack_index][-1])) # reference to the block underneath in new arrangement
                       # print("|IF I>0... New Arrangement: ", temp_stacks, " Block underneath: ", temp_stacks[goal_stack_index][-1], " Moves: ", moves)
                        #input("Press Enter to continue...")
                    else:
                        moves.append((block, goal_stack[0]))
                       # print("| ELSE ... Moves: ", goal_stack)
                        #input("Press Enter to continue...")
                       

                    move_block(block, "Table", goal_stack_index)
                    print_state()

        return moves