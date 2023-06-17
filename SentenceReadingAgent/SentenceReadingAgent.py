import re
import time

class SentenceReadingAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        self.word_tags = {
            'Serena':'PROPN',
            'Andrew':'PROPN',
            'Bobbie':'PROPN',
            'Cason':'PROPN',
            'David':'PROPN',
            'Farzana':'PROPN',
            'Frank':'PROPN',
            'Hannah':'PROPN',
            'Ida':'PROPN',
            'Irene':'PROPN',
            'Jim':'PROPN',
            'Jose':'PROPN',
            'Keith':'PROPN',
            'Laura':'PROPN',
            'Lucy':'PROPN',
            'Meredith':'PROPN',
            'Nick':'PROPN',
            'Ada':'PROPN',
            'Yeeling':'VERB',
            'Yan':'PROPN',
            'the':'PRON',
            'of':'ADP',
            'to':'PART',
            'and':'CCONJ',
            'a':'PRON',
            'in':'ADP',
            'is':'AUX',
            'it':'PRON',
            'you':'PRON',
            'that':'PRON',
            'he':'PRON',
            'was':'AUX',
            'for':'ADP',
            'on':'ADP',
            'are':'AUX',
            'with':'ADP',
            'as':'ADP',
            'I':'PRON',
            'his':'PRON',
            'they':'PRON',
            'be':'AUX',
            'at':'ADP',
            'one':'NUM',
            'have':'VERB',
            'this':'PRON',
            'from':'ADP',
            'or':'CCONJ',
            'had':'VERB',
            'by':'ADP',
            'hot':'ADJ',
            'but':'CCONJ',
            'some':'PRON',
            'what':'PRON',
            'there':'ADV',
            'we':'PRON',
            'can':'AUX',
            'out':'ADV',
            'other':'ADJ',
            'were':'AUX',
            'all':'PRON',
            'your':'PRON',
            'when':'SCONJ',
            'up':'ADV',
            'use':'VERB',
            'word':'NOUN',
            'how':'SCONJ',
            'said':'VERB',
            'an':'PRON',
            'each':'PRON',
            'she':'PRON',
            'which':'PRON',
            'do':'VERB',
            'their':'PRON',
            'time':'NOUN',
            'if':'SCONJ',
            'will':'AUX',
            'way':'NOUN',
            'about':'ADV',
            'many':'ADJ',
            'then':'ADV',
            'them':'PRON',
            'would':'AUX',
            'write':'VERB',
            'like':'INTJ',
            'so':'ADV',
            'these':'PRON',
            'her':'PRON',
            'long':'ADV',
            'make':'VERB',
            'thing':'NOUN',
            'see':'VERB',
            'him':'PRON',
            'two':'NUM',
            'has':'VERB',
            'look':'VERB',
            'more':'ADV',
            'day':'NOUN',
            'could':'AUX',
            'go':'VERB',
            'come':'VERB',
            'did':'VERB',
            'my':'PRON',
            'sound':'NOUN',
            'no':'INTJ',
            'most':'ADV',
            'number':'NOUN',
            'who':'PRON',
            'over':'ADP',
            'know':'VERB',
            'water':'NOUN',
            'than':'ADP',
            'call':'VERB',
            'first':'ADV',
            'people':'NOUN',
            'may':'AUX',
            'down':'ADV',
            'side':'NOUN',
            'been':'AUX',
            'now':'ADV',
            'find':'VERB',
            'any':'PRON',
            'new':'ADJ',
            'work':'NOUN',
            'part':'NOUN',
            'take':'VERB',
            'get':'VERB',
            'place':'NOUN',
            'made':'VERB',
            'live':'VERB',
            'where':'SCONJ',
            'after':'ADP',
            'back':'ADV',
            'little':'ADJ',
            'only':'ADV',
            'round':'ADV',
            'man':'NOUN',
            'year':'NOUN',
            'came':'VERB',
            'show':'VERB',
            'every':'PRON',
            'good':'ADJ',
            'me':'PRON',
            'give':'VERB',
            'our':'PRON',
            'under':'ADP',
            'name':'NOUN',
            'very':'ADV',
            'through':'ADP',
            'just':'ADV',
            'form':'VERB',
            'much':'ADV',
            'great':'ADJ',
            'think':'VERB',
            'say':'VERB',
            'help':'VERB',
            'low':'ADJ',
            'line':'NOUN',
            'before':'ADP',
            'turn':'VERB',
            'cause':'VERB',
            'same':'ADJ',
            'mean':'VERB',
            'differ':'VERB',
            'move':'VERB',
            'right':'INTJ',
            'boy':'PROPN',
            'old':'ADJ',
            'too':'ADV',
            'does':'VERB',
            'tell':'VERB',
            'sentence':'VERB',
            'set':'VERB',
            'three':'NUM',
            'want':'VERB',
            'air':'NOUN',
            'well':'INTJ',
            'also':'ADV',
            'play':'VERB',
            'small':'ADJ',
            'end':'NOUN',
            'put':'VERB',
            'home':'NOUN',
            'read':'VERB',
            'hand':'VERB',
            'port':'NOUN',
            'large':'ADJ',
            'spell':'VERB',
            'add':'VERB',
            'even':'ADV',
            'land':'NOUN',
            'here':'ADV',
            'must':'AUX',
            'big':'ADJ',
            'high':'ADJ',
            'such':'ADJ',
            'follow':'VERB',
            'act':'VERB',
            'why':'SCONJ',
            'ask':'VERB',
            'men':'NOUN',
            'change':'VERB',
            'went':'VERB',
            'light':'ADJ',
            'kind':'VERB',
            'off':'ADV',
            'need':'VERB',
            'house':'NOUN',
            'picture':'NOUN',
            'try':'VERB',
            'us':'PRON',
            'again':'ADV',
            'animal':'NOUN',
            'point':'VERB',
            'mother':'NOUN',
            'world':'NOUN',
            'near':'ADP',
            'build':'VERB',
            'self':'NOUN',
            'earth':'NOUN',
            'father':'PROPN',
            'head':'NOUN',
            'stand':'VERB',
            'own':'ADJ',
            'page':'NOUN',
            'should':'AUX',
            'country':'NOUN',
            'found':'VERB',
            'answer':'NOUN',
            'school':'NOUN',
            'grow':'VERB',
            'study':'VERB',
            'still':'ADV',
            'learn':'VERB',
            'plant':'NOUN',
            'cover':'VERB',
            'food':'NOUN',
            'sun':'PROPN',
            'four':'NUM',
            'thought':'VERB',
            'let':'VERB',
            'keep':'VERB',
            'eye':'NOUN',
            'never':'ADV',
            'last':'ADJ',
            'door':'NOUN',
            'between':'ADP',
            'city':'NOUN',
            'tree':'NOUN',
            'cross':'VERB',
            'since':'SCONJ',
            'hard':'ADV',
            'start':'VERB',
            'might':'AUX',
            'story':'NOUN',
            'saw':'VERB',
            'far':'ADV',
            'sea':'NOUN',
            'draw':'VERB',
            'left':'VERB',
            'late':'ADV',
            'run':'VERB',
            'don�t':'PROPN',
            'while':'SCONJ',
            'press':'NOUN',
            'close':'VERB',
            'night':'NOUN',
            'real':'ADJ',
            'life':'NOUN',
            'few':'ADJ',
            'stop':'VERB',
            'open':'VERB',
            'seem':'VERB',
            'together':'ADV',
            'next':'ADV',
            'white':'PROPN',
            'children':'NOUN',
            'begin':'VERB',
            'got':'VERB',
            'walk':'VERB',
            'example':'NOUN',
            'ease':'NOUN',
            'paper':'NOUN',
            'often':'ADV',
            'always':'ADV',
            'music':'NOUN',
            'those':'PRON',
            'both':'PRON',
            'mark':'NOUN',
            'book':'NOUN',
            'letter':'NOUN',
            'until':'ADP',
            'mile':'NOUN',
            'river':'NOUN',
            'car':'NOUN',
            'feet':'NOUN',
            'care':'VERB',
            'second':'ADV',
            'group':'NOUN',
            'carry':'VERB',
            'took':'VERB',
            'rain':'NOUN',
            'eat':'VERB',
            'room':'NOUN',
            'friend':'NOUN',
            'began':'VERB',
            'idea':'NOUN',
            'fish':'NOUN',
            'mountain':'NOUN',
            'north':'NOUN',
            'once':'ADV',
            'base':'NOUN',
            'hear':'VERB',
            'horse':'NOUN',
            'cut':'VERB',
            'sure':'ADV',
            'watch':'VERB',
            'color':'NOUN',
            'face':'VERB',
            'wood':'NOUN',
            'main':'ADJ',
            'enough':'ADV',
            'plain':'ADV',
            'girl':'NOUN',
            'usual':'ADJ',
            'young':'ADJ',
            'ready':'ADJ',
            'above':'ADP',
            'ever':'ADV',
            'red':'adj',
            'list':'NOUN',
            'though':'SCONJ',
            'feel':'VERB',
            'talk':'VERB',
            'bird':'NOUN',
            'soon':'ADV',
            'body':'NOUN',
            'dog':'NOUN',
            'family':'NOUN',
            'direct':'VERB',
            'pose':'VERB',
            'leave':'VERB',
            'song':'NOUN',
            'measure':'NOUN',
            'state':'NOUN',
            'product':'NOUN',
            'black':'ADJ',
            'short':'ADJ',
            'numeral':'ADJ',
            'class':'NOUN',
            'wind':'NOUN',
            'question':'NOUN',
            'happen':'VERB',
            'complete':'ADJ',
            'ship':'NOUN',
            'area':'NOUN',
            'half':'NOUN',
            'rock':'NOUN',
            'order':'NOUN',
            'fire':'NOUN',
            'south':'PROPN',
            'problem':'NOUN',
            'piece':'NOUN',
            'told':'VERB',
            'knew':'VERB',
            'pass':'VERB',
            'farm':'NOUN',
            'top':'ADJ',
            'whole':'ADJ',
            'king':'NOUN',
            'size':'NOUN',
            'heard':'VERB',
            'best':'ADJ',
            'hour':'NOUN',
            'better':'ADV',
            'TRUE':'ADJ',
            'during':'ADP',
            'hundred':'NUM',
            'am':'AUX',
            'remember':'VERB',
            'step':'NOUN',
            'early':'ADV',
            'hold':'VERB',
            'west':'PROPN',
            'ground':'NOUN',
            'interest':'NOUN',
            'reach':'VERB',
            'fast':'VERB',
            'five':'NUM',
            'sing':'VERB',
            'listen':'VERB',
            'six':'NUM',
            'table':'NOUN',
            'travel':'NOUN',
            'less':'ADV',
            'morning':'NOUN',
            'ten':'NUM',
            'simple':'ADJ',
            'several':'ADJ',
            'vowel':'VERB',
            'toward':'ADP',
            'war':'NOUN',
            'lay':'VERB',
            'against':'ADP',
            'pattern':'NOUN',
            'slow':'ADJ',
            'center':'NOUN',
            'love':'NOUN',
            'person':'NOUN',
            'money':'NOUN',
            'serve':'VERB',
            'appear':'VERB',
            'road':'NOUN',
            'map':'NOUN',
            'science':'NOUN',
            'rule':'NOUN',
            'govern':'VERB',
            'pull':'VERB',
            'cold':'ADJ',
            'notice':'VERB',
            'voice':'NOUN',
            'fall':'VERB',
            'power':'NOUN',
            'town':'NOUN',
            'fine':'ADJ',
            'certain':'ADJ',
            'fly':'VERB',
            'unit':'NOUN',
            'lead':'VERB',
            'cry':'PROPN',
            'dark':'ADJ',
            'machine':'NOUN',
            'note':'NOUN',
            'wait':'VERB',
            'plan':'NOUN',
            'figure':'NOUN',
            'star':'NOUN',
            'box':'PROPN',
            'noun':'PROPN',
            'field':'NOUN',
            'rest':'NOUN',
            'correct':'ADJ',
            'able':'ADJ',
            'pound':'NOUN',
            'done':'VERB',
            'beauty':'NOUN',
            'drive':'VERB',
            'stood':'VERB',
            'contain':'VERB',
            'front':'NOUN',
            'teach':'VERB',
            'week':'NOUN',
            'final':'ADJ',
            'gave':'VERB',
            'green':'ADJ',
            'oh':'INTJ',
            'quick':'ADJ',
            'develop':'VERB',
            'sleep':'NOUN',
            'warm':'ADJ',
            'free':'ADJ',
            'minute':'NOUN',
            'strong':'ADJ',
            'special':'ADJ',
            'mind':'NOUN',
            'behind':'ADP',
            'clear':'ADJ',
            'tail':'VERB',
            'produce':'VERB',
            'fact':'NOUN',
            'street':'PROPN',
            'inch':'NOUN',
            'lot':'NOUN',
            'nothing':'PRON',
            'course':'NOUN',
            'stay':'VERB',
            'wheel':'NOUN',
            'full':'ADJ',
            'force':'NOUN',
            'blue':'ADJ',
            'object':'NOUN',
            'decide':'VERB',
            'surface':'NOUN',
            'deep':'ADV',
            'moon':'NOUN',
            'island':'NOUN',
            'foot':'NOUN',
            'yet':'ADV',
            'busy':'ADJ',
            'test':'NOUN',
            'record':'NOUN',
            'boat':'NOUN',
            'common':'ADJ',
            'gold':'NOUN',
            'possible':'ADJ',
            'plane':'NOUN',
            'age':'NOUN',
            'dry':'ADJ',
            'wonder':'VERB',
            'laugh':'VERB',
            'thousand':'NUM',
            'ago':'ADV',
            'ran':'VERB',
            'check':'VERB',
            'game':'NOUN',
            'shape':'NOUN',
            'yes':'INTJ',
            'cool':'ADJ',
            'miss':'VERB',
            'brought':'VERB',
            'heat':'NOUN',
            'snow':'NOUN',
            'bed':'NOUN',
            'bring':'VERB',
            'sit':'VERB',
            'perhaps':'ADV',
            'fill':'VERB',
            'east':'NOUN',
            'weight':'NOUN',
            'language':'NOUN',
            'among':'ADP',
            'Red':'PROPN',
            'adults':'NOUN',
            'wrote':'VERB',
            'sings':'NOUN',
            'dog\'s':'NOUN',
            'written':'VERB'
        }
        pass

    def solve(self, sentence, question):
        # Add your code here! Your solve method should receive
        # two strings as input: sentence and question. It should
        # return a string representing the answer to the question.
        # Load word classifications from file
        start_time = time.time()
        word_tags = self.word_tags

        # Sentence and Question preprocessing
        sentence = re.sub(r'[.,?\'"]', '', sentence)  
        question = re.sub(r'[.,?\'"]', '', question).lower()
    
        # map words of each sentence to their tag (e.g., "NOUN")
        sentence_words = sentence.split()
        sentence_tags = [word_tags.get(word) for word in sentence_words]
        sentence_tags = [tag for tag in sentence_tags]  

        # Check for time in sentence and add the tag "TIME"
        time_words = re.search(r'\b\d{1,2}:\d{2}(AM|PM)?\b', sentence)
        if time_words:
            index = sentence_words.index(time_words.group())
            sentence_tags[index] = 'TIME'

        # Identify the type of question
        question_words = question.split()
        question_type = 'unknown'
        
        if 'who' in question_words:
            question_type = 'who'
        elif 'at' in question_words:
            question_type = 'at'
        elif 'what' in question_words:
                question_type = 'what'
        elif 'how' in question_words:
                question_type = 'how'
        elif 'where' in question_words:
            question_type = 'where'
        elif 'when' in question_words:
            question_type = 'when'
        
    
        answer = None
  
        if question_type == 'who':
            # If the question includes "did" or "does", and "to", return the PROPN that is not present in the question.
            if ('did' in question_words or 'does' in question_words) and 'to' in question_words:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag in ['PROPN'] and word.lower() not in question_words:
                        elapsed_time = time.time() - start_time
                        print(question_type, " time: ", elapsed_time)
                        return word

            # Identify if the sentence has another verb
            verb = [word for word in sentence_words if word_tags.get(word, '') == 'VERB']
            if verb:
                verb_index = sentence_words.index(verb[0])

                # If the question includes "was", return the NOUN or PROPN that comes after the verb in the sentence.
                if 'was' in question_words:
                    for word, tag in zip(sentence_words[verb_index+1:], sentence_tags[verb_index+1:]):
                        if tag in ['PROPN', 'NOUN']:
                            elapsed_time = time.time() - start_time
                            print(question_type," time: ", elapsed_time)
                            return word
                        
                else:
                    for word, tag in zip(reversed(sentence_words[:verb_index]), reversed(sentence_tags[:verb_index])):
                        elapsed_time = time.time() - start_time
                        print(question_type," time: ", elapsed_time)
                        return word
                    

        if question_type == 'where':
            # Check if there is a (PART) in the sentence
            part_index = [index for index, tag in enumerate(sentence_tags) if tag == 'PART']
            if part_index:
                # Return the first noun
                for word, tag in zip(sentence_words[part_index[-1]+1:], sentence_tags[part_index[-1]+1:]):
                    if tag == 'NOUN':
                        elapsed_time = time.time() - start_time
                        print(question_type," time: ", elapsed_time)
                        return word

            # check if there is an adposition (ADP) in the sentence
            adp_index = [index for index, tag in enumerate(sentence_tags) if tag == 'ADP']
            if adp_index:
                # Return the first noun that appears after the last adposition, unless the adposition is "of"
                for index in reversed(adp_index):
                    if sentence_words[index].lower() == 'of':
                        if index > 0 and sentence_tags[index - 1] == 'NOUN':
                            elapsed_time = time.time() - start_time
                            print(question_type," time: ", elapsed_time)
                            return sentence_words[index - 1]
                    else:
                        for word, tag in zip(sentence_words[index+1:], sentence_tags[index+1:]):
                            if tag == 'NOUN':
                                elapsed_time = time.time() - start_time
                                print(question_type," time: ", elapsed_time)
                                return word

        if question_type == 'what':
            for i, word in enumerate(sentence_words):
                if (word in question_words or sentence_tags[i] == 'ADJ'): # check that the word is in the question or tagged as ADJ
                    if i + 1 < len(sentence_words) and sentence_tags[i + 1] == 'NOUN':
                        elapsed_time = time.time() - start_time
                        print(question_type," time: ", elapsed_time)
                        return sentence_words[i + 1]  # return the noun AFTER the ADJ

            if 'color' in question_words:
                for i, word in enumerate(sentence_words):
                    if sentence_tags[i] == 'AUX': # check that the word is tagged as AUX
                        if i + 1 < len(sentence_words) and sentence_tags[i + 1] == 'ADJ': # check if the previous word is a noun
                            elapsed_time = time.time() - start_time
                            print(question_type," time: ", elapsed_time)
                            return sentence_words[i + 1]  # return the noun BEFORE the AUX

            elif 'name' in question_words:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag in ['PROPN']:
                        elapsed_time = time.time() - start_time
                        print(question_type," time: ", elapsed_time)
                        return word

            else:
                verb_index = [i for i, tag in enumerate(sentence_tags) if tag == 'VERB']
                if verb_index:
                    # Return the noun that comes before the verb in the sentence.
                    for word, tag in zip(reversed(sentence_words[:verb_index[0]]), reversed(sentence_tags[:verb_index[0]])):
                        if tag == 'NOUN':
                            elapsed_time = time.time() - start_time
                            print(question_type," time: ", elapsed_time)
                            return word
                        
   
                    
                
                        
        elif question_type == 'how':
            # If the question is "how long", return the adjective.
            if 'long' in question_words:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag == 'ADJ':
                        elapsed_time = time.time() - start_time
                        print(question_type," time: ", elapsed_time)
                        return word
            # If the question is "how far", return the noun.
            elif 'far' in question_words:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag == 'NOUN':
                        elapsed_time = time.time() - start_time
                        print(question_type," time: ", elapsed_time)
                        return word
            # If the question is "how many" type, return the number.
            elif 'many' in question_words:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag == 'NUM':
                        elapsed_time = time.time() - start_time
                        print(question_type," time: ", elapsed_time)
                        return word
            # If the question is "how"  with "do" but without "at"
            elif 'do' in question_words and 'at' not in question_words:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag == 'VERB':
                        elapsed_time = time.time() - start_time
                        print(question_type," time: ", elapsed_time)
                        return word
                    
        elif question_type == 'at':
        # If the question is "at" , find a time.
            time_match = re.search(r'\b\d{1,2}:\d{2}(AM|PM)?\b', sentence)
            if time_match:
                elapsed_time = time.time() - start_time
                print(question_type," time: ", elapsed_time)
                return time_match.group()

        else:
            elapsed_time = time.time() - start_time
            print(question_type," time: ", elapsed_time)
            answer = 'I dont know'
            
        return answer