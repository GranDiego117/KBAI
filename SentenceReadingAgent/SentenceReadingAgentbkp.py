import spacy
import re

class SentenceReadingAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def solve(self, sentence, question):
        # Add your code here! Your solve method should receive
        # two strings as input: sentence and question. It should
        # return a string representing the answer to the question.

        # Load the spaCy language model
        self.nlp = spacy.load('en_core_web_sm')

        # Process the sentence and the question with spaCy. This returns a Doc object that contains a lot of linguistic information.
        sentences = self.nlp(sentence)
        questions = self.nlp(question)

        # Extract the question type (first word in the question).
        qtype = questions[0].lower_

        # Based on the question type, try to find the answer in the sentence.
        if qtype == 'who':
            # If the question is a "who did what to whom" type
            if 'did' in [token.lower_ for token in questions]:
                # Get the verb from the question.
                verb = [token.lemma_ for token in questions if token.pos_ == 'VERB']
                # If 'to' is in the question, return the object of 'to' from the sentence.
                if 'to' in [token.lower_ for token in questions]:
                    for token in sentences:
                        if token.dep_ == 'pobj' and token.head.text == 'to':
                            return token.text
                else:
                    # If 'to' is not in the question, return the direct object of the verb in the sentence.
                    for token in sentences:
                        if token.head.lemma_ in verb and token.dep_ in ['dobj', 'iobj']:
                            return token.text
            else:
                # If the question is a "who is doing what" type, return the subject of the sentence.
                for token in sentences:
                    if token.dep_ in ['nsubj', 'nsubjpass']:
                        return token.text

        elif qtype == 'what':
            # If the question is a "what" type, return the direct object of the sentence.
            for token in sentences:
                if token.dep_ == 'dobj':
                    return token.text

        elif qtype == 'where':
            # If the question is a "where" type, return the object of the preposition in the sentence.
            for token in sentences:
                if token.dep_ == 'prep':
                    for child in token.children:
                        if child.dep_ in ['pobj']:
                            return child.text

        elif qtype == 'how':
            # If the question is a "how long" type, return the adjective modifier in the sentence.
            if 'long' in [token.lower_ for token in questions]:
                for token in sentences:
                    if token.dep_ in ['amod']:
                        return token.text
            # If the question is a "how far" type, return the noun phrase adverbial modifier in the sentence.
            elif 'far' in [token.lower_ for token in questions]:
                for token in sentences:
                    if token.dep_ == 'npadvmod':
                        return token.text
            elif 'do' in [token.lower_ for token in questions] and 'at' not in [token.lower_ for token in questions]:
                for token in sentences:
                    if token.dep_ in ['ROOT']:
                        return token.text
                    
        elif qtype == 'at':
            # If the question is an "at" type, try to find a time format in the sentence.
            time_match = re.search(r"\b\d{1,2}:\d{2}(AM|PM)?\b", sentence)
            if time_match:
                return time_match.group()

        return "I don't know."