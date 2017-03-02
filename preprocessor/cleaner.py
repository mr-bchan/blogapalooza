
import re
import threading


import stop_words as stop
from nltk.stem import WordNetLemmatizer

class Preprocessor:

    instance = None

    def __init__(self):
        if not Preprocessor.instance:
            Preprocessor.instance = Preprocessor.Preprocessor_Singleton()

        else:
            print "Warning, this is a singleton. Using existing singleton instance."

    def __getattr__(self, name):
        return getattr(self.instance, name)
    #
    # def cleanMePlease(self, tweet):
    #     if not Preprocessor.instance:
    #         Preprocessor.instance = Preprocessor.Preprocessor_Singleton()
    #
    #     print 'initialization complete! '
    #     Preprocessor.instance.cleanMePlease(tweet)

    class Preprocessor_Singleton:

        instance = None

        wordnet_lemmatizer = None

        stop_words = None

        tokens_re = None

        lock = threading.Lock()

        def __init__(self):

                print "Creating singleton instance."

                self.wordnet_lemmatizer = WordNetLemmatizer()

                # get stopwords from stop_words package and provide additional stop words
                additional_stop_words = ['hello', 'hi', 'just', 'can', 've', 'll', 'nt', 'get', 'got', 'shall', 'still',
                                         'didn', 'aren', 're', 'don', 'isn', 'please', 'us', 'ain\'t', 'th', 'also',
                                         'will']
                self.stop_words = stop.get_stop_words('english')
                self.stop_words.extend(additional_stop_words)



                regex_str = [
                    r'<[^>]+>',  # HTML tags
                    r'(?:[\w_d]+[.|\w_d]*@[\w_d]+.[\w_d]+[.[\w_d]+]*)',  # email address
                    r'(?:\\u[\wd_]+[\\u[\wd_]+]*)',  # emojis in unicode format
                    r'(?:\\x[\wd_]+[\\x[\wd_]+]*)',  # emojis in unicode format
                    r'(?:\\\w)',  # escape characters
                    r'(?:@[\w_]+)',  # @-mentions
                    r'(?:&[\w_]+)',  # &-mentions
                    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
                    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
                    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
                    r"(?:[a-z][a-z\-_]+[a-z])",  # words with - and '
                    r'(?:[\w_]+)',  # other words
                    r'(?:\S)'  # anything else
                ]

                self.tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)



        def hasNumbers(self, inputString):
          return any(char.isdigit() for char in inputString)

        # @timing
        def lemmatize(self, word) :
                output = self.wordnet_lemmatizer.lemmatize(word)
                return output


        def tokenize(self, s):
            s = s.lower()
            self.tokens_re.findall(s)
            return self.tokens_re.findall(s)

        def clean_tokens(self, tokens):

            clean_tokens = []

            for token in tokens:


                if(token[0:2] == '\U'): # emoji unicode format
                    clean_tokens.append('<emoji:'+ token + '>')

                if token[0] == '\\' : #mentions and escape characters
                    continue

                if len(token) == 1: #one word, punctuation marks
                    continue

                if token[0] == 'a' and self.hasNumbers(token[1]):
                    continue

                if self.hasNumbers(token[0]) == True: #remove words with starting numbers
                    continue

                if token in self.stop_words: #remove other stop words
                    continue

                if token[0] in ['<', '>']:  # remove html tags
                    continue

                if token[0] == '#':
                    clean_tokens.append(self.lemmatize(token.lower()[1:]))

                if(token[len(token)-1] == '.'):
                    token = token[0:len(token)-1]
                    if len(token) > 1:
                        clean_tokens.append(self.lemmatize((token.lower())))

                else:

                    token = self.lemmatize(token.decode('utf-8'))
                    split_tokens = token.lower().strip().split()
                    clean_tokens.extend(split_tokens)


            return clean_tokens

        def cleanMePlease(self,tweet):

            self.lock.acquire()

            try:
                tweet = tweet.encode('unicode_escape')

                tokens = self.tokenize(tweet)

                tokens = self.clean_tokens(tokens)

                return tokens

            finally:

                self.lock.release()

