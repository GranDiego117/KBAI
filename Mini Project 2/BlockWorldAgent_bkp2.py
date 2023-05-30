class BlockWorldAgent:
    def __init__(self):
        pass

    def solve(self, initial_arrangement, goal_arrangement):
        
        moves = []
        current_arrangement = []
        
        for blocks in initial_arrangement:
            new_arrangement = list(blocks)
            current_arrangement.append(new_arrangement)

        block_positions = {}
        
        for i, stack in enumerate(current_arrangement):
            for block in stack:
                block_positions[block] = i
        
        print(" Current Arrangement: ", current_arrangement, " Goal arrangement: ", goal_arrangement)

        while current_arrangement != goal_arrangement:
            for goals in reversed(goal_arrangement):
                for block in reversed(goals):
                    position = block_positions[block]
                    
                    print("| Current Block: ", block, "Current Position: ", position if position != "Table" else "On the Table", " Goal Stack: ", goal_arrangement.index(goals),  "Goal Position in Stack: ", goals.index(block))
                    
                    # If the block is not in the correct stack or if it is not in the correct position within the stack
                    if position != goal_arrangement.index(goals) or (position != "Table" and current_arrangement[position].index(block) != goals.index(block)):

                        # If the block is not on the table, move blocks that are on top of it to the table
                        if position != "Table":
                            while current_arrangement[position][-1] != block:
                                top_block = current_arrangement[position].pop()
                                moves.append((top_block, "Table"))
                                block_positions[top_block] = "Table"
                                print("|| Moving block: ", top_block, " on top of current block: ", block, "to the Table")

                        # Move the block to the table
                        if position != "Table":
                            current_arrangement[position].remove(block)
                            moves.append((block, "Table"))
                            block_positions[block] = "Table"
                            print("|| Moving current block: ", block, " to the Table")
                    
                    # If the block is on the table, move it to the correct stack
                    if block_positions[block] == "Table":
                        current_arrangement[goal_arrangement.index(goals)].append(block)
                        if len(goals) > 1:
                            moves.append((block, goals[0]))
                            print("|| Moving current block: ", block, " to the stack on top of: ", goals[0])
                        else:
                            moves.append((block, "Table"))
                            print("|| Moving current block: ", block, " to the new stack")
                        block_positions[block] = goal_arrangement.index(goals)

                    # If the block is in its correct stack but not in the correct position, move it to the table
                    # Make sure the block is in the current arrangement before trying to find its index
                    if position != "Table" and block in current_arrangement[position] and current_arrangement[position].index(block) != goals.index(block):
                        current_arrangement[position].remove(block)
                        moves.append((block,"Table"))
                        block_positions[block] = "Table"
                        print("||Moving current block: ", block, " to the Table")

        return moves