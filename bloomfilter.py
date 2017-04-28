import zlib


class BloomFilter:
    """
    A bloom filter is a data structure to answer yes or no questions very fast
    Especially to check the membership of a value in the set
    """

    def __init__(self, size, hashCount):
        """
        Initialize a bit array where each element is 0 
        Pick the size of the bit array to be the number of members in the set
        """
        if hashCount > size:
            raise Exception("Number of hashes must be less than the size.")

        self.bitArray = 0
        self.length = size
        self.hashCount = hashCount

    def getBaseHash(self, word):

        return zlib.crc32(word.encode('utf-8')) % self.length

    def insert(self, word):
        """
        :param word: Insert words into the bloom filter
        :return None: 
        """
        # hashX0 = self.getBaseHash(word)
        #
        # # double hashing
        # hashX1 = hashX0 + 2 * hashX0
        # hashX2 = hashX0 + hashX1 * 3
        # hashX3 = hashX0 + hashX1 + 4 * hashX2
        # hashX4 = hashX0 + hashX1 + hashX2 + hashX3 * 5
        # hashX5 = hashX0 + hashX1 + hashX2 + hashX3 + hashX4 * 6
        # hashX6 = hashX0 + hashX1 + hashX2 + hashX3 + hashX4 + hashX5 * 7

        hashValues = self.generateHashes(word)

        for curHash in hashValues:
            self.bitArray |= 1 << curHash


            # self.bitArray |= 1 << hashX0
            # self.bitArray |= 1 << hashX1
            # self.bitArray |= 1 << hashX2
            # self.bitArray |= 1 << hashX3
            # self.bitArray |= 1 << hashX4
            # self.bitArray |= 1 << hashX5
            # self.bitArray |= 1 << hashX6

    def isMember(self, lookup):

        # hashX0 = self.getBaseHash(lookup)
        # hashX1 = hashX0 + (2 * hashX0)
        # hashX2 = hashX0 + hashX1 * 3
        # hashX3 = hashX0 + hashX1 + 4 * hashX2
        # hashX4 = hashX0 + hashX1 + hashX2 + hashX3 * 5
        # hashX5 = hashX0 + hashX1 + hashX2 + hashX3 + hashX4 * 6
        # hashX6 = hashX0 + hashX1 + hashX2 + hashX3 + hashX4 + hashX5 * 7

        hashValues = self.generateHashes(lookup)

        for hashVal in hashValues:
            if (self.bitArray >> hashVal) & 1 != 1:
                return False
        return True

        # if (self.bitArray >> hashX0) & 1 == 1 and (self.bitArray >> hashX1) & 1 == 1 \
        #             (self.bitArray >> hashX2) & 1 == 1 and (self.bitArray >> hashX3) & 1 == 1 \
        #             (self.bitArray >> hashX4) & 1 == 1 and (self.bitArray >> hashX5) & 1 == 1 \
        #             (self.bitArray >> hashX6) & 1 == 1:
        #     return True
        # return False

    def __str__(self):
        return bin(self.bitArray)

    def generateHashes(self, word):
        hashes = []
        i = 2;

        hashes.append(self.getBaseHash(word))

        for j in range(1,self.hashCount):
            newHash = (hashes[j - 1] + (i * hashes[(0 if (j - 2) < 0 else (j - 2))])) % self.length
            i += 1
            hashes.append(newHash)

        return hashes
