class BlockWorldAgent:
    def __init__(self):
        pass

    def solve(self, initial_arrangement, goal_arrangement):
        moves = []
        table = []

        def print_state():
            print(f"Current arrangement: {initial_arrangement}")
            print(f"Table: {table}")
            print(f"Goal arrangement: {goal_arrangement}")
            print("--------------------------------------------------")

        def move_block(block, source, destination):
            if source == "Table":
                table.remove(block)
            else:
                initial_arrangement[source].remove(block)

            if destination == "Table":
                table.append(block)
            else:
                initial_arrangement[destination].append(block)

        # Move all blocks to the table first
        for stack in initial_arrangement:
            while stack:
                moves.append((stack[-1], "Table"))
                table.append(stack.pop())
                print_state()
                input("Press Enter to continue...")

        # Move blocks from the table to their respective positions
        for goal_stack in goal_arrangement:
            for block in goal_stack:
                if block in table:
                    destination_stack_idx = goal_arrangement.index(goal_stack)
                    moves.append((block, "Table"))
                    move_block(block, "Table", destination_stack_idx)
                    print_state()
                    input("Press Enter to continue...")

        # Move blocks from the table to their final positions in the goal arrangement
        for goal_stack in goal_arrangement:
            for i, block in enumerate(goal_stack):
                if block in table:
                    moves.append((block, goal_stack[i-1]))
                    move_block(block, "Table", goal_stack[i-1])
                    print_state()
                    input("Press Enter to continue...")

        return moves