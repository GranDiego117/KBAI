from SentenceReadingAgent import SentenceReadingAgent

def test():
    #This will test your SentenceReadingAgent
	#with nine initial test cases.

    test_agent = SentenceReadingAgent()

    sentence_1 = "Ada brought a short note to Irene."
    question_1 = "Who brought the note?"
    question_2 = "What did Ada bring?"
    question_3 = "Who did Ada bring the note to?"
    question_4 = "How long was the note?"

    sentence_2 = "David and Lucy walk one mile to go to school every day at 8:00AM when there is no snow."
    question_5 = "Who does Lucy go to school with?"
    question_6 = "Where do David and Lucy go?"
    question_7 = "How far do David and Lucy walk?"
    question_8 = "How do David and Lucy get to school?"
    question_9 = "At what time do David and Lucy walk to school?"

    sentence_3 = "The white dog and the blue horse play together."
    question_10 = "What animal is blue?"

    sentence_4 = "The water is blue."
    question_11 = "What color is the water?"

    sentence_5 = "She told her friend a story"
    question_12 = "Who was told a story?"

    sentence_6 = "My dog Red is very large."
    question_13 = "What is my dog's name?"

    sentence_7 = "She will write him a love letter."
    question_14 = "What will she write to him?"

    sentence_8 = "The sound of rain is cool."
    question_15 = "What is cool?"

    sentence_9 = "Bring the dog to the other room."
    question_16 = "Where should the dog go?"

    sentence_10 = "There are one hundred adults in that city."
    question_17 = "Where are the adults?"

    sentence_11 = "She told her friend a story."
    question_18 = "Who told a story?"

    sentence_12 = "The island is east of the city."
    question_19 = "Where is the island?"

    sentence_13 = "There are three men in the car."
    question_20 = "How many men are in the car?"

    sentence_14 = "Serena ran a mile this morning."
    question_21 = "When did Serena run?"

    sentence_15 = "There are a thousand children in this town."
    question_22 = "How many children are in this town?"

    sentence_16 = "This tree came from the island."
    question_23 = "What came from the island?"

    sentence_17 = "The white dog and the blue horse play together."
    question_24 = "What do the dog and horse do?"

    print(test_agent.solve(sentence_1, question_1), " | Ada")  # "Ada"
    print(test_agent.solve(sentence_1, question_2), " | note")  # "note" or "a note"
    print(test_agent.solve(sentence_1, question_3), " | Irene")  # "Irene"
    print(test_agent.solve(sentence_1, question_4), " | short")  # "short"

    print(test_agent.solve(sentence_2, question_5), " | David")  # "David"
    print(test_agent.solve(sentence_2, question_6), " | school")  # "school"
    print(test_agent.solve(sentence_2, question_7), " | mile")  # "mile" or "a mile"
    print(test_agent.solve(sentence_2, question_8), " | walk")  # "walk"
    print(test_agent.solve(sentence_2, question_9), " | 8:00AM")  # "8:00AM"

    print(test_agent.solve(sentence_3, question_10), " | horse") # horse

    print(test_agent.solve(sentence_4, question_11), " | blue") # blue

    print(test_agent.solve(sentence_5, question_12), " | her friend") # friend

    print(test_agent.solve(sentence_6, question_13), " | Red") # letter

    print(test_agent.solve(sentence_7, question_14), " | letter") # sound

    print(test_agent.solve(sentence_8, question_15), " | sound") # other room

    print(test_agent.solve(sentence_9, question_16), " | room") # city

    print(test_agent.solve(sentence_10, question_17), " | city") # She

    print(test_agent.solve(sentence_11, question_18), " | she") # east

    print(test_agent.solve(sentence_12, question_19), " | east")

    print(test_agent.solve(sentence_13, question_20), " | three")

    print(test_agent.solve(sentence_14, question_21), " | morning")

    print(test_agent.solve(sentence_15, question_22), " | thousand")

    print(test_agent.solve(sentence_16, question_23), " | tree")

    print(test_agent.solve(sentence_17, question_24), " | play")

if __name__ == "__main__":
    test()