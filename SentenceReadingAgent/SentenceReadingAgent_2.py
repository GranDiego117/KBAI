import re

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

        #print(sentence)
        print(question)

        word_tags = self.word_tags

        # Save the word-tag pairs in a new .txt file
        with open('wordtags.txt', 'w') as f:
            for word, tag in word_tags.items():
                f.write(f'{word} {tag}\n')

        # Preprocess the sentence and question by removing punctuation and converting to lower case
        sentence = re.sub(r'[.,?\'"]', '', sentence)  # remove full stops, question marks, commas, and apostrophes
        question = re.sub(r'[.,?\'"]', '', question).lower() # remove full stops, question marks, commas, and apostrophes
    
         # Tokenize the sentence and map words to their part-of-speech
        sentence_words = sentence.split()
        sentence_tags = [word_tags.get(word) for word in sentence_words]
        sentence_tags = [tag for tag in sentence_tags]  # convert words to lower case
        #print(sentence_tags)

        # Check for time in sentence
        time_in_sentence = re.search(r'\b\d{1,2}:\d{2}(AM|PM)?\b', sentence)
        if time_in_sentence:
            time_index = sentence_words.index(time_in_sentence.group())
            sentence_tags[time_index] = 'TIME'

        # Identify the type of question
        question_words = question.split()
        question_type = 'unknown'
        #print(" QUESTION: ", question)
        if 'who' in question_words:
            question_type = 'who'
        elif 'at' in question_words:
            question_type = 'at'
        elif 'what' in question_words:
                question_type = 'what'
        elif 'how' in question_words:
            if 'much' in question_words:
                question_type = 'how_much'
            elif 'many' in question_words:
                question_type = 'how_many'
            else:
                question_type = 'how'
        elif 'where' in question_words:
            question_type = 'where'
        elif 'when' in question_words:
            question_type = 'when'
        
        
        # Check if we have a noun or a proper noun already present in the question
        #print("QUESTION TYPE: ", question_type)
        #print("SENTENCE: ",sentence_words, sentence_tags)

        # Generate the answer based on the question type
        answer = None

        
        if question_type == 'who':
            if 'did' in question_words:
                verb = [word for word in question_words if word_tags.get(word, '').lower() == 'verb']
                if 'to' in question_words:
                    for index, word in enumerate(sentence_words):
                        if word.lower() == 'to':
                            if index + 1 < len(sentence_words):
                                return sentence_words[index + 1]
            else:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag == 'NOUN':
                        if word.lower() != 'time':
                            return word
                    else:
                        return word
            if 'told' in question_words:
                for i, word in enumerate(sentence_words):
                    if word.lower() == 'told':
                        if i + 1 < len(sentence_words) and 'was' in question_words:
                            return sentence_words[i + 1]
                        elif i > 0:
                            return sentence_words[i - 1]
            
                        

        if question_type == 'what':
            if 'color' in question_words:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag in ['ADJ']:
                        return word
            elif 'name' in question_words:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag in ['PROPN']:
                        return word
            else:
                for i, word in enumerate(sentence_words):
                    if word_tags.get(word, '') in ['ADJ', 'PROPN'] and word in question_words:
                        if i + 1 < len(sentence_words) and word_tags.get(sentence_words[i+1], '').lower() == 'noun':
                            return sentence_words[i + 1]
                    elif word_tags.get(word, '') in ['NOUN']:
                        if i + 1 < len(sentence_words) and word_tags.get(sentence_words[i+1], '').lower() == 'noun':
                            return sentence_words[i + 1]
                        else:
                            return word
        
        if question_type == 'where':
            if 'of' in sentence_words:
                for i, word in enumerate(sentence_words):
                    if word.lower() == 'of':
                        if i > 0:
                            return sentence_words[i - 1]
            else:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag in ['NOUN', 'PROPN']:
                        if 'place' in word_tags.get(word, ''):
                            return word
                        elif 'city' in word.lower():
                            return word
                        elif 'room' in word.lower():
                            return word
                
                        
        elif question_type == 'how':
            # If the question is a "how long" type, return the adjective modifier in the sentence.
            if 'long' in question_words:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag == 'ADJ':
                        return word
            # If the question is a "how far" type, return the noun phrase adverbial modifier in the sentence.
            elif 'far' in question_words:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag == 'NOUN':
                        return word
            # If the question is a "how" type with "do" but without "at"
            elif 'do' in question_words and 'at' not in question_words:
                for word, tag in zip(sentence_words, sentence_tags):
                    if tag == 'VERB':
                        return word
                    
        elif question_type == 'at':
        # If the question is an "at" type, try to find a time format in the sentence.
            time_match = re.search(r'\b\d{1,2}:\d{2}(AM|PM)?\b', sentence)
            if time_match:
                return time_match.group()

        else:
            # If we can't determine the type of the question, return 'I don't know'
            answer = 'I dont know'
            
        return answer