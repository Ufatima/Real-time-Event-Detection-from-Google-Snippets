from __future__ import unicode_literals
from nltk.corpus import stopwords
import re
from string import punctuation

with open('twitter_en.txt', 'r') as f:
    stopwords_list = []
    for line in f:
        stopwords_list.append(line)
    stopwords_list[:] = [line.rstrip('\n') for line in stopwords_list]

stopwords = set(stopwords.words('english'))
pun = list(punctuation)


class tf_idf(object):
    def __init__(self):
        # self.docs = docs
        pass

    def stripNonAlphaNum(self, text):
        texts = re.compile(r'\W+', re.UNICODE).split(text)
        return texts

    def removeStopwords(self, wordlist, stopwords):
        text = [w for w in wordlist if w not in stopwords]
        text = [w for w in text if not w.isnumeric()]
        return text

    def remove_punctuaions(self, wordlist, pun):
        text = [w for w in wordlist if w not in pun]
        return text

    def wordListToFreqDict(self, fullwordlist):
        wordfreq = [fullwordlist.count(p) for p in fullwordlist]
        return dict(zip(fullwordlist, wordfreq))

    def sortFreqDict(self, dictionary):
        aux = [(dictionary[key], key) for key in dictionary]
        aux.sort()
        aux.reverse()
        return aux

    def generate_tfidf_topic(self, doc_complete):
        text_string = ', '.join(doc_complete)
        fullwordlist = self.stripNonAlphaNum(text_string)
        word_list = self.removeStopwords(fullwordlist, stopwords)
        word_list = [w for w in word_list if w not in stopwords_list]
        word_list = self.remove_punctuaions(word_list, pun)
        dictionary = self.wordListToFreqDict(word_list)
        sortdict = self.sortFreqDict(dictionary)
        # extracted top 3 terms considered as an event
        top3_terms = sortdict[:3]
        tfIdf_event = []
        for s in sortdict[:3]:
            tfIdf_event.append(s[1])
        return tfIdf_event

    def generate_tfIdf_frequency_array(self, doc_complete):
        wordlist = []
        for doc in doc_complete:
            doc = doc.replace("#", "").replace("_", " ")  # Removing HASH symbol
            doc = re.sub(r'[^\x00-\x7f]', r'', doc)  # Removing the Hex characters(emoji)
            stop_free = " ".join([i for i in doc.lower().split() if i not in stopwords])
            stop_free = " ".join([i for i in stop_free.lower().split() if i not in stopwords_list])
            text = re.sub(r'[^a-zA-Z0-9@\S]', ' ', stop_free) # removing punctuations
            remove_pun = str.maketrans({key: None for key in punctuation})
            punc_free = text.translate(remove_pun)
            f = punc_free.split()
            wordlist.append(f)
        fullwordlist = []
        for item in wordlist:
            if isinstance(item, (str, int, bool)):
                fullwordlist.append(item)
            elif isinstance(item, dict):
                for i in item.items():
                    fullwordlist.extend(i)
            else:
                fullwordlist.extend(list(item))
        print(fullwordlist)
        dictionary = self.wordListToFreqDict(fullwordlist)
        sortdict = self.sortFreqDict(dictionary)
        return sortdict