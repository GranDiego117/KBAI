import time

class MonsterClassificationAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        self.default_attributes = {
            'size': [],
            'color': [],
            'covering': [],
            'foot-type': [],
            'leg-count': [],
            'arm-count': [],
            'eye-count': [],
            'horn-count': [],
            'lays-eggs': [],
            'has-wings': [],
            'has-gills': [],
            'has-tail': []
        }


    def solve(self, samples, new_monster):
        #Add your code here!
        #
        #The first parameter to this method will be a labeled list of samples in the form of
        #a list of 2-tuples. The first item in each 2-tuple will be a dictionary representing
        #the parameters of a particular monster. The second item in each 2-tuple will be a
        #boolean indicating whether this is an example of this species or not.
        #
        #The second parameter will be a dictionary representing a newly observed monster.
        #
        #Your function should return True or False as a guess as to whether or not this new
        #monster is an instance of the same species as that represented by the list.

        
        # Create the positive and negative sample lists
        start_time = time.time()
        positive_samples = {key: [] for key in self.default_attributes.keys()}
        negative_samples = {key: [] for key in self.default_attributes.keys()}
        
        # Check each sample monster and their attributes
        for sample, is_positive in samples:
            for attribute, value in sample.items():
                # add to default_attributes if it has not been seen before
                if value not in self.default_attributes[attribute]:
                    self.default_attributes[attribute].append(value)
                # If this is a positive example, add this attribute value to positive_samples
                if is_positive:
                    positive_samples[attribute].append(value)
                # Add it to negative_samples
                else:
                    negative_samples[attribute].append(value)

        # Create weighted index for both positive and negative samples
        positive_index = self.build_weighted_index(positive_samples)
        negative_index = self.build_weighted_index(negative_samples)

        # Rank the positive attributes by importance (frequency)
        positive_ranking = sorted([(k, v) for k, v in positive_index.items() if k[0] in new_monster],
                                  key=lambda x: x[1], reverse=True)
        #print("Positive Ranking: ", positive_ranking)

        score = 0
        # Go through all attributes of the new_monster
        for attribute, value in new_monster.items():
            #print(" Attribute: ", attribute)

            # Get  scores of attribute value in positive and negative samples
            positive_score = positive_index.get((attribute, value), 0)
            negative_score = negative_index.get((attribute, value), 0)

            #print("Attribute: ", attribute," Positive Attribute: ", positive_score, " Negative Attribute: ", negative_score )

            # If attribute is new
            if positive_score == 0 and negative_score == 0:
                # And among the most important attributes in positive samples, penalize the final score
                if (attribute, value) in positive_ranking[:len(positive_ranking) // 2]:
                    score -= 0.005
                # If it's among the least important attributes, then add to the final score
                else:
                    score += 0.005
            else:
                score += positive_score - negative_score

        # If the final score is positive, new monster is likely from same species
        elapsed_time = time.time() - start_time
        print("time: ", elapsed_time)
        return score > 0 

    def build_weighted_index(self, samples):
        index = {}

        for attribute, values in samples.items():
            for value in values:
                # Increment count for each attribute found in sample
                index[(attribute, value)] = index.get((attribute, value), 0) + 1

        total = sum(index.values())
        # Get weighted scores
        for key in index:
            index[key] /= total
                
        return index