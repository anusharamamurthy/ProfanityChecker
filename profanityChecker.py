import bloomfilter as bloom
import math
import pickle
import string


# Stop words to remove during processing the documents.
# Some are taken from the internet and modified to suit our model.
# https://github.com/Alir3z4/python-stop-words

stopWords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'arent', 'as',
            'at', 'because', 'be', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cant',
            'cannot',
            'couldnt', 'did', 'didnt', 'do', 'does', 'doesnt', 'doing', 'dont', 'down', 'during', 'each', 'few', 'for',
            'from',
            'further', 'had', 'hadnt', 'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed', 'hell', 'hes', 'her',
            'hers', 'here',
            'heres', 'herself', 'him', 'himself', 'his', 'how', 'hows', 'i', 'id', 'ill', 'im', 'ive', 'if', 'in',
            'into', 'is', 'isnt',
            'it', 'its', 'itself', 'lets', 'more', 'me', 'most', 'mustnt', 'my', 'myself', 'no', 'nor', 'not', 'of',
            'off', 'on', 'once',
            'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shant', 'she',
            'shell', 'shed', 'shes',
            'should', 'shouldnt', 'so', 'some', 'such', 'than', 'that', 'thats', 'the', 'their', 'theirs', 'them',
            'themselves', 'then',
            'there', 'theres', 'they', 'theyd', 'theyll', 'theyre', 'theyve', 'this', 'those', 'though', 'through',
            'to', 'too', 'under',
            'until', 'up', 'very', 'was', 'wasnt', 'we', 'wed', 'well', 'were', 'weve', 'werent', 'what', 'whats',
            'when', 'whens', 'where',
            'wheres', 'which', 'while', 'who', 'whos', 'whom', 'why', 'whys', 'with', 'wont', 'would', 'wouldnt',
            'you', 'youd', 'youll',
            'youre', 'youve', 'your', 'yours', 'yourself', 'yourselves', 'font', 'html', 'table', 'br', 'will',
            'article', 'says', 'can', 'one', 'use', 'writes']

class ProfanityChecker():

    def getWords(self, fname):

        with open(fname, 'r') as fp:
            line = fp.readlines()
        fp.close()
        return line

    def getText(self, fname):

        with open(fname, 'r') as fp:
            line = fp.readlines()
        fp.close()
        return line

    def pickleFilter(self, instance,fname):

        pkl = open(fname, 'wb')
        pickle.dump(instance, pkl)
        pkl.close()

    def unPickleFilter(self,fname):

        pkl = open(fname, 'rb')
        self.myFilter = pickle.load(pkl)
        pkl.close()

    def setUp(self):

        """set up bloom filter to insert profane words"""
        words = self.getWords("profanity_en.txt")
        self.myFilter = bloom.BloomFilter(2000, 3)
        for word in words:
            self.myFilter.insert(word.strip().lower())

    def sanitize_content(self,content):

        content = content.lower()
        rmv = string.punctuation + '\t\n'
        translator = str.maketrans('', '', rmv)
        content = content.translate(translator)
        # content = content.translate(string.digits)
        sanitized_content = [word for word in content.split() if word not in stopWords]
        return sanitized_content



    def testMembership(self):

        """
        check for the number of false positives
        """
        # self.setUp()
        # self.pickleFilter(self.myFilter,"BloomFilter")
        self.unPickleFilter("BloomFilter")

        # flag text for review
        flagged = []
        text = "This is sweet. They should shut up."


        parsedText = self.sanitize_content(text)

        for word in parsedText:
            if self.myFilter.isMember(word):
                flagged.append(word)

        print("These words are flagged:")
        print(flagged)

    def calOptArrayLen(self):

        setLen = eval(input("Please enter the size of your set:"))
        errRate = float(input("Please enter the acceptable false positive rate[0.0 - 1.0]:"))

        bArrLen = (setLen * math.log(errRate, math.e)) / (math.log(2, math.e) ** 2)

        kfnc = (bArrLen * math.log(2, math.e)) / setLen

        print("Optimal Bit Vector Length is:", abs(math.floor(bArrLen)))
        print("Optimal number of Hash functions is:", abs(math.floor(kfnc)))


if __name__ == '__main__':
    myCheck = ProfanityChecker()
    myCheck.testMembership()
