class MonsterDiagnosisAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def solve(self, diseases, patient):
        # Add your code here!
        #
        # The first parameter to this method is a list of diseases, represented as a
        # list of 2-tuples. The first item in each 2-tuple is the name of a disease. The
        # second item in each 2-tuple is a dictionary of symptoms of that disease, where
        # the keys are letters representing vitamin names ("A" through "Z") and the values
        # are "+" (for elevated), "-" (for reduced), or "0" (for normal).
        #
        # The second parameter to this method is a particular patient's symptoms, again
        # represented as a dictionary where the keys are letters and the values are
        # "+", "-", or "0".
        #
        # This method should return a list of names of diseases that together explain the
        # observed symptoms. If multiple lists of diseases can explain the symptoms, you
        # should return the smallest list. If multiple smallest lists are possible, you
        # may return any sufficiently explanatory list.

        print("Patient: ", patient)

        smallest_diagnosis = None

        # List of disease names.
        disease_list = list(diseases.keys())

        # Total number of diseases.
        total_diseases = len(disease_list)

        max_iterations = min(1 << total_diseases, 1000000)

        # Loop through all possible combinations of diseases (brute force approach).
        for i in range(max_iterations):
            print("Iteration: ", i)

            current_disease_combination = []

            # Make the combinations of all diseases (one by one will be checked with the posible solution)
            for j in range(total_diseases):
                if (i & (1 << j)) != 0:
                    current_disease_combination.append(disease_list[j])
                    print("Current diseases: ", current_disease_combination)

            symptom_counts = {}
            for i in range(26):  # Go from 0 to 25.
                char = chr(i + ord('A'))  # Convert number to corresponding letter.
                symptom_counts[char] = 0  # Start the count for this symptom at 0.

            # iterate over each effect to determine whether or not we should change the vitamin (-1, 0, +1)
            for disease in current_disease_combination:
                print("Looking at disease:", disease)
                for vitamin, effect in diseases[disease].items():
                    # Increment, decrement, or leave the count alone based on the effect (+/-).
                    if effect == "+":
                        symptom_counts[vitamin] += 1
                    elif effect == "-":
                        symptom_counts[vitamin] -= 1
                    else:
                        pass
                    print("Vitamin: ", vitamin, " Effect: ", effect, " symptom counts: ", symptom_counts[vitamin])

            # Check if the symptom counts match the patient's symptoms.
            is_match = True
            for vitamin, count in symptom_counts.items():
                # Decide on the expected effect based on the count.
                if count == 0:
                    expected_effect = '0'
                elif count > 0:
                    expected_effect = '+'
                else:
                    expected_effect = '-'
                
                # If the expected effect does not match the actual effect, it is not a match.
                if expected_effect != patient[vitamin]:
                    is_match = False
                    break

            # If we found a match and it's smaller than the smallest one found so far, then it's the right match.
            if is_match:
                if smallest_diagnosis is None:
                    smallest_diagnosis = list(current_disease_combination)
                elif len(current_disease_combination) < len(smallest_diagnosis):
                    smallest_diagnosis = list(current_disease_combination)

        return smallest_diagnosis