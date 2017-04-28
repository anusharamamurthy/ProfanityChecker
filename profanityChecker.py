import bloomfilter as bloom
import math
import unittest
import pickle

class Test(unittest.TestCase):

    @classmethod
    def getWords(self,fname):

        with open(fname, 'r') as fp:
            line = fp.readlines()
        fp.close()
        return line

    def getText(self,fname):

        with open(fname, 'r') as fp:
            line = fp.readlines()
        fp.close()
        return line

    def pickleFilter(self,instance):

        pkl = open("bloomFilter.pkl",'wb')
        pickle.dump(instance,pkl)
        pkl.close()

    def unPickleFilter(self):

        pkl = open("bloomFilter.pkl",'rb')
        self.myFilter = pickle.load(pkl)
        pkl.close()

    def setUp(self):

        """set up bloom filter to insert profane words"""
        words = self.getWords("profanity_en.txt")
        self.myFilter = bloom.BloomFilter(4173)
        for word in words:
            self.myFilter.insert(word.strip().lower())

    def testMembership(self):
        """
        check for the number of false positives
        """
        # self.setUp()
        # self.pickleFilter(self.myFilter)
        self.unPickleFilter()
        text = self.getText("/Users/aramamurthy/Downloads/Github/ProfanityChecker/Brennan-Greenstadt-Corpus/a/a_01.txt")
        falsePos = []
        for words in text:
            for word in words.split():
                if self.myFilter.isMember(word.lower()):
                    falsePos.append(word)


        # self.calOptArrayLen()


    def calOptArrayLen(self):

        setLen = eval(input("Please enter the size of your set:"))
        errRate = float(input("Please enter the acceptable false positive rate[0.0 - 1.0]:"))

        bArrLen = (setLen * math.log(errRate,math.e)) / (math.log(2,math.e)**2)

        kfnc = (bArrLen * math.log(2,math.e)) / setLen

        print("Optimal Bit Vector Length is:",abs(math.floor(bArrLen)))
        print("Optimal number of Hash functions is:",abs(math.floor(kfnc)))


if __name__ == '__main__':
    unittest.main()

