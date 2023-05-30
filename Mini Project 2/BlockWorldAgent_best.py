class BlockWorldAgent:
    def __init__(self):
        pass

    def solve(self, initial_arrangement, goal_arrangement):
        initial_arrangement = [stack.copy() for stack in initial_arrangement]
        moves = []
        table = []
        new_arrangement = [[] for _ in range(len(goal_arrangement))]

        def print_state():
            print(f"Current arrangement: {initial_arrangement}")
            print(f"Table: {table}")
            print(f"New arrangement: {new_arrangement}")
            print(f"Goal arrangement: {goal_arrangement}")
            print(f"Moves: {moves}")
            print("--------------------------------------------------")

        def move_block(block, source, destination):
            if source != "Table":
                initial_arrangement[source].remove(block)
            else:
                table.remove(block)
            if destination != "Table":
                new_arrangement[destination].append(block)
            else:
                table.append(block)

        for stack in initial_arrangement:
            while stack:
                block_to_move = stack[-1]
                goal_stack_index = None
               # print("Stack: ", stack, " bloack to move: ", block_to_move)
               # input("Press Enter to continue...")
                    
                for index, goal_stack in enumerate(goal_arrangement):
                    if block_to_move in goal_stack:
                        goal_stack_index = index
                      #  print("block to move: ", block_to_move, " is in the goal stack ", goal_stack, " in stack ", goal_stack_index)
                      #  input("Press Enter to continue...")
                        break
                    
                if goal_stack_index is not None:
                    block_position_in_goal_stack = goal_arrangement[goal_stack_index].index(block_to_move)
                   # print("Block Position in Goal Stack:  ", goal_arrangement[goal_stack_index].index(block_to_move) )
                   # input("Press Enter to continue...")
                    if block_position_in_goal_stack > 0: # Block to move is not the base in goal
                        block_below = goal_arrangement[goal_stack_index][block_position_in_goal_stack - 1]
                        if block_below in new_arrangement[goal_stack_index]:
                            moves.append((block_to_move, block_below))
                            move_block(block_to_move, initial_arrangement.index(stack), goal_stack_index)
                        else:
                            moves.append((block_to_move, 'Table'))
                            table.append(stack.pop())
                    else:
                        if(stack.index(block_to_move) > 0):
                            moves.append((block_to_move, 'Table'))
                        move_block(block_to_move, initial_arrangement.index(stack), goal_stack_index)
                       # print("Block ", block_to_move, " is currently in ", initial_arrangement.index(stack), " and moving to: ", goal_stack_index)
                       # input("Press Enter to continue...")
                else:
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
                    if i > 0 and new_arrangement[goal_stack_index][-1] != goal_stack[i - 1]:
                       # print("|IF i>0... new arrangement: ", new_arrangement, " goal_stack_index ", goal_stack_index, " goal stack ", goal_stack)
                        #input("Press Enter to continue...")
                        continue

                    if i > 0:
                        moves.append((block, new_arrangement[goal_stack_index][-1])) # reference to the block underneath in new arrangement
                       # print("|IF I>0... New Arrangement: ", new_arrangement, " Block underneath: ", new_arrangement[goal_stack_index][-1], " Moves: ", moves)
                        #input("Press Enter to continue...")
                    else:
                        moves.append((block, goal_stack[0]))
                       # print("| ELSE ... Moves: ", goal_stack)
                        #input("Press Enter to continue...")
                       

                    move_block(block, "Table", goal_stack_index)
                    print_state()

        return moves


