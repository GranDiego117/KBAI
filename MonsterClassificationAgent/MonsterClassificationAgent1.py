from collections import Counter 
import time

class MonsterClassificationAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        self.monsterDefault = {
            'size': ['tiny', 'small', 'medium', 'large', 'huge'],
            'color': ['black', 'white', 'brown', 'gray', 'red', 'yellow', 'blue', 'green', 'orange', 'purple'],
            'covering': ['fur', 'feathers', 'scales', 'skin'],
            'foot-type': ['paw', 'hoof', 'talon', 'foot', 'none'],
            'leg-count': [0, 1, 2, 3, 4, 5, 6, 7, 8],
            'arm-count': [0, 1, 2, 3, 4, 5, 6, 7, 8],
            'eye-count': [0, 1, 2, 3, 4, 5, 6, 7, 8],
            'horn-count': [0, 1, 2],
            'lays-eggs': [True, False],
            'has-wings': [True, False],
            'has-gills': [True, False],
            'has-tail': [True, False]
            }


        self.monster_has = {}
        self.monster_doesnt_have = {}
        self.count_dict = {}


    def find_ranks(self, monsters):
        count_dict = {}
        max_size =  max(set([monsters['size']]), key = monsters['size'].count)
        max_color=  max(set([monsters['color']]), key = monsters['color'].count)
        max_covering =  max(set([monsters['covering']]), key = monsters['covering'].count)
        max_foot_type =  max(set([monsters['foot-type']]), key = monsters['foot-type'].count)
        max_arm_count =  max(set([monsters['arm-count']]), key = lambda x: x)
        max_eye_count =  max(set([monsters['eye-count']]), key = lambda x: x)
        max_horn_count =  max(set([monsters['horn-count']]), key = lambda x: x)
        max_wings_count =  max(set([monsters['has-wings']]), key = lambda x: x)
        max_gills_count =  max(set([monsters['has-gills']]), key = lambda x: x)
        max_tails_count =  max(set([monsters['has-tail']]), key = lambda x: x)
        max_eggs_count =  max(set([monsters['lays-eggs']]), key = lambda x: x)
        max_leg_count =  max(set([monsters['leg-count']]), key = lambda x: x)

        print([max_size,max_color,max_covering,max_foot_type,max_arm_count,max_eye_count,
        max_horn_count,max_horn_count,max_wings_count, max_gills_count, max_tails_count,max_eggs_count,
        max_leg_count])

        self.count_dict['size'] = max_size
        self.count_dict['color'] = max_color
        self.count_dict['covering'] = max_covering
        self.count_dict['foot-type'] = max_foot_type
        self.count_dict['leg-count'] = max_leg_count
        self.count_dict['arm-count'] = max_arm_count
        self.count_dict['eye-count'] = max_eye_count
        self.count_dict['horn-count'] = max_horn_count
        self.count_dict['lays-eggs'] = max_eggs_count
        self.count_dict['has-wings'] = max_wings_count
        self.count_dict['has-gills'] = max_wings_count
        self.count_dict['has-tail'] = max_tails_count

        return self.count_dict



    def solve(self, samples, new_monster):
        start_time = time.time()

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
        for monster in samples:
            # monster_attributes = {y:x for x,y in monster[0].items()}
            # print(monster_attributes)
            # monster_attributes = monster[0].items()
            monster_attributes = list(monster[0].items())
            # print(monster_attributes)

            if monster[1] == True:
                self.monster_has['size'] = monster_attributes[0][1]
                self.monster_has['color'] = monster_attributes[1][1]
                self.monster_has['covering'] = monster_attributes[2][1]
                self.monster_has['foot-type'] = monster_attributes[3][1]
                self.monster_has['leg-count'] = monster_attributes[4][1]
                self.monster_has['arm-count'] = monster_attributes[5][1]
                self.monster_has['eye-count'] = monster_attributes[6][1]
                self.monster_has['horn-count'] = monster_attributes[7][1]
                self.monster_has['lays-eggs'] = monster_attributes[8][1]
                self.monster_has['has-wings'] = monster_attributes[9][1]
                self.monster_has['has-gills'] = monster_attributes[10][1]
                self.monster_has['has-tail'] = monster_attributes[11][1]

                

            self.monster_doesnt_have['size'] = [x for x in list(self.monsterDefault['size'])  if x !=self.monster_has['size']] 
            self.monster_doesnt_have['color'] = [x for x in list(self.monsterDefault['color'])  if x !=self.monster_has['color']] 
            self.monster_doesnt_have['covering'] = [x for x in list(self.monsterDefault['covering'])  if x !=self.monster_has['covering']] 
            self.monster_doesnt_have['foot-type'] = [x for x in list(self.monsterDefault['foot-type'])  if x !=self.monster_has['foot-type']] 
            self.monster_doesnt_have['leg-count'] = [x for x in list(self.monsterDefault['leg-count'])  if x !=self.monster_has['leg-count']] 
            self.monster_doesnt_have['arm-count'] = [x for x in list(self.monsterDefault['arm-count'])  if x !=self.monster_has['arm-count']] 
            self.monster_doesnt_have['eye-count'] = [x for x in list(self.monsterDefault['eye-count'])  if x !=self.monster_has['eye-count']] 
            self.monster_doesnt_have['horn-count'] = [x for x in list(self.monsterDefault['horn-count'])  if x !=self.monster_has['horn-count']] 
            self.monster_doesnt_have['lays-eggs'] = [x for x in list(self.monsterDefault['lays-eggs'])  if x !=self.monster_has['lays-eggs']] 
            self.monster_doesnt_have['has-wings'] = [x for x in list(self.monsterDefault['has-wings'])  if x !=self.monster_has['has-wings']] 
            self.monster_doesnt_have['has-gills'] = [x for x in list(self.monsterDefault['has-gills'])  if x !=self.monster_has['has-gills']] 
            self.monster_doesnt_have['has-tail'] = [x for x in list(self.monsterDefault['has-tail'])  if x !=self.monster_has['has-tail']] 
                
            print(self.monster_has['foot-type'])

          
        ranked_dict = ((self.find_ranks(self.monster_has))) ## the most common version of a monster

        value = { k : ranked_dict.items() for k in set(ranked_dict.items()) - set(new_monster.items()) }

        ## diff between out monster and the average monster
        
        print(len(list(value.values())))

        diff = (len(list(value)))
        print(diff)

        print(new_monster)
        print(self.monster_has)

        if diff == 0:
            return True
            print("--- %s seconds ---" % (time.time() - start_time))

        elif diff == 1:
            return True
            print("--- %s seconds ---" % (time.time() - start_time))

        elif diff == 2:
            print("--- %s seconds ---" % (time.time() - start_time))

            return True          
        elif diff == 3:
            print("--- %s seconds ---" % (time.time() - start_time))

            return True
        elif diff == 4:
            print("--- %s seconds ---" % (time.time() - start_time))

            return True
        elif diff == 5:
            print("--- %s seconds ---" % (time.time() - start_time))

            return True
        elif diff == 6:
            print("--- %s seconds ---" % (time.time() - start_time))

            return False
        elif diff == 7:
            print("--- %s seconds ---" % (time.time() - start_time))

            return False
        elif diff == 8:
            print("--- %s seconds ---" % (time.time() - start_time))

            return False
        elif diff == 9:
            print("--- %s seconds ---" % (time.time() - start_time))

            return False
        elif diff == 10:
            print("--- %s seconds ---" % (time.time() - start_time))

            return False
        elif diff == 11:
            print("--- %s seconds ---" % (time.time() - start_time))

            return False
        else:
            print("--- %s seconds ---" % (time.time() - start_time))
            
            return False



        # print(score)
        # if score < 0.70:
        #     return True
        # else:
        #     return False





# known_positive_1 = {'size': 'huge', 'color': 'black', 'covering': 'fur', 'foot-type': 'paw', 'leg-count': 2, 'arm-count': 4, 'eye-count': 2, 'horn-count': 0, 'lays-eggs': True, 'has-wings': True, 'has_gills': True, 'has-tail': True}
# new_monster_1 = {'size': 'large', 'color': 'black', 'covering': 'fur', 'foot-type': 'paw', 'leg-count': 1, 'arm-count': 3, 'eye-count': 2, 'horn-count': 0, 'lays-eggs': True, 'has-wings': True, 'has_gills': True, 'has-tail': True}
# known_positive_2 = {'size': 'large', 'color': 'white', 'covering': 'fur', 'foot-type': 'paw', 'leg-count': 2, 'arm-count': 4, 'eye-count': 2, 'horn-count': 0, 'lays-eggs': True, 'has-wings': True, 'has_gills': True, 'has-tail': False}

# m = MonsterClassificationAgent([known_positive_1,known_positive_2,])