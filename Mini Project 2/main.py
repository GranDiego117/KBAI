from BlockWorldAgent import BlockWorldAgent

def test():
    #This will test your BlockWorldAgent
	#with eight initial test cases.
    test_agent = BlockWorldAgent()

    initial_arrangement_1 = [["A", "B", "C"], ["D", "E"]]
    #initial_arrangement_1 = [['C', 'H', 'B', 'D'], ['F', 'I', 'A'], ['E', 'J'], ['G']]
    #goal_arrangement_1 = [['C', 'H', 'G'], ['D', 'I', 'A'], ['E', 'F', 'B'], ['J']]
    goal_arrangement_1 = [["A", "C"], ["D", "E", "B"]]
    goal_arrangement_2 = [["A", "B", "C", "D", "E"]]
    goal_arrangement_3 = [["D", "E", "A", "B", "C"]]
    goal_arrangement_4 = [["C", "D"], ["E", "A", "B"]]

    print(test_agent.solve(initial_arrangement_1, goal_arrangement_1))
    print(test_agent.solve(initial_arrangement_1, goal_arrangement_2))
    print(test_agent.solve(initial_arrangement_1, goal_arrangement_3))
    print(test_agent.solve(initial_arrangement_1, goal_arrangement_4))

    initial_arrangement_2 = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
    goal_arrangement_5 = [["A", "B", "C", "D", "E", "F", "G", "H", "I"]]
    goal_arrangement_6 = [["I", "H", "G", "F", "E", "D", "C", "B", "A"]]
    goal_arrangement_7 = [["H", "E", "F", "A", "C"], ["B", "D"], ["G", "I"]]
    goal_arrangement_8 = [["F", "D", "C", "I", "G", "A"], ["B", "E", "H"]]

    print(test_agent.solve(initial_arrangement_2, goal_arrangement_5))
    print(test_agent.solve(initial_arrangement_2, goal_arrangement_6))
    print(test_agent.solve(initial_arrangement_2, goal_arrangement_7))
    print(test_agent.solve(initial_arrangement_2, goal_arrangement_8))



    initial_arrangement_3 = [['I', 'J', 'C', 'B'], ['F', 'E', 'A', 'K'], ['H', 'D', 'G']]
    goal_arrangement_9 = [['J', 'D', 'I'], ['F'], ['H'], ['K', 'G', 'E'], ['B', 'C', 'A']]

    print(test_agent.solve(initial_arrangement_3, goal_arrangement_9))

if __name__ == "__main__":
    test()