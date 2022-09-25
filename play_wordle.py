import numpy as np

class PlayWorldle(object):
    """
    Class for Wordle Helper.
    """
    
    def __init__(self, all_words):
        print('<<< Welcome to a new Worldle! >>>')
        self.all_words = all_words           # all words in dictionary
        self.remaining_words = all_words     # remaining words
        self.guesses = []                    # guesses
        self.game_state = 0
        self.remaining_words_log = dict()
        self.remaining_words_log[0] = len(self.remaining_words)

    def enter_guess(self, 
                    guess, 
                    green_chars, 
                    amber_chars):
        
        self.guesses = self.guesses + [guess]
        correct = self.correct_dict(guess, 
                                    green_chars, 
                                    amber_chars)

        print('Correct letters:')
        print(correct)

        incorrect = [c for c in guess if c not in correct]

        print('Incorrect letters:')
        print(incorrect)
        
        remaining_words = self.remaining_words

        incorrect_words = []
        for word in remaining_words:
            word_correct = True
            while(word_correct == True): 
                for char in correct:
                    for i in correct[char]:
                        if i > 0:
                            idx = i-1
                            if word[idx] == char:
                                continue
                            else:
                                word_correct = False
                                incorrect_words.append(word)
                                break
                        else:
                            idx = abs(i)-1
                            if (word[idx] != char) & (char in word):
                                continue
                            else:
                                word_correct = False
                                incorrect_words.append(word)
                                break
                for char in incorrect:
                    if (char in word):
                        incorrect_words.append(word)
                        break    
                break   

        remaining_words = [w for w in remaining_words if w not in incorrect_words]

        print("Remaining words ({}) ".format(len(remaining_words)))     
        if len(remaining_words)<=5:
            print(remaining_words) 
            if len(remaining_words)==1:
                print('Congratulations...eliminated down to one!')

        self.remaining_words = remaining_words
        self.game_state += 1
        self.remaining_words_log[self.game_state] = len(remaining_words)
        

    def gen_char_entropy(self):

        words_remaining = self.remaining_words
        words_all = self.all_words
        n_words = len(words_remaining)
        unique_chars = set([c for c in ''.join(words_all)])

        entropy = dict.fromkeys(unique_chars, 0)

        # get freq of letters in each word
        for char in unique_chars:
            n = 0
            for word in words_remaining:
                if char in word:
                    n += 1
            if (n_words-n != 0) & (n != 0):
                entropy[char] = (-(n/n_words)*np.log2(n/n_words) 
                                 - ((n_words-n)/n_words)*np.log2((n_words-n)/n_words))
            else:
                entropy[char] = 0

        return entropy 

        
    def gen_word_entropy(self, return_best=None, show=None):
        
        words_remaining = self.remaining_words
        
        if len(words_remaining) == 2:
            print('Only two possible words left!')
            best_choices = words_remaining
            if show:
                print('Here are the best guesses...')
                for i in best_choices:
                    print([i])
        else:         
            words = self.all_words
            word_entropy = dict.fromkeys(words, 0)
            char_ent = self.gen_char_entropy()

            for w in words:
                entropy = 0
                used_chars = []
                for c in w:
                    if c not in used_chars:
                        entropy = entropy + char_ent[c]
                        used_chars.append(c)
                word_entropy[w] = entropy/len(w)

            best_choices = sorted(word_entropy, key=word_entropy.get, reverse=True)[:10]

            if word_entropy[best_choices[0]] == 0:
                print('Best entropy is 0...are all remaining words anagrams?')

            if show:
                print('Here are the best guesses...')
                for i in best_choices:
                    print([i, word_entropy[i]])

        if return_best:
            return best_choices

    def correct_dict(self, guess, green_chars, amber_chars):
        
        try:
            correct = dict()
            for char in green_chars:
                correct[char] = [guess.index(char)+1]
            for char in amber_chars:
                correct[char] = [-1*(guess.index(char)+1)]
            return correct
        except:
            raise Exception('Tried to add letter(s) not in guess!')