import zlib, math


class BloomFilter:
    """
    A bloom filter is a data structure to answer yes or no questions very fast
    Especially to check the membership of a value in the set
    """

    def __init__(self, size, hash_count):

        """
        Initialize a Bloom Filter
        :param size: Size of the array
        :param hashCount: The number of hash functions to use
        
        >>> filter = BloomFilter(10,11)
        Traceback (most recent call last):
        ...
        Exception: Number of hashes must be less than the size.
        
        >>> filter = BloomFilter(10,9)
        
        """

        if hash_count > size:
            raise Exception("Number of hashes must be less than the size.")

        self.bit_array = 0
        self.length = size
        self.hash_count = hash_count

    def get_base_hash(self, word):
        """
        
        :param word: individual word
        :return hash: a hash value for the word
        """

        return zlib.crc32(word.encode('utf-8')) % self.length

    def insert(self, word):
        """
        :param word: Inserts words into the bloom filter
        :return None: 
        >>> tf.insert("dont")
        >>> tf.insert("use")
        >>> tf.insert("these")
        >>> tf.insert("words")
        """

        hash_values = self.generate_hashes(word)

        for cur_hash in hash_values:
            self.bit_array |= 1 << cur_hash

    def is_member(self, lookup):
        """
        Checks if a word is in the Bloom filter.
        :param lookup: The word to look up.
        :return: True if the word exists in the filter. False otherwise. 
                 Note that Bloom filters suffer from false positives.
        
        >>> tf.is_member("dont")
        True
        >>> tf.is_member("bad")
        False
        """

        hash_values = self.generate_hashes(lookup)

        for hash_val in hash_values:
            if (self.bit_array >> hash_val) & 1 != 1:
                return False
        return True

    def __str__(self):
        """
        Convert the data structure into binary string format for better visualization.
        :return: The Binary format of bitArray as a string
        
        >>> len("{0:b}".format(tf.bit_array)) <= tf.length
        True
        """
        return bin(self.bit_array)

    def generate_hashes(self, word):
        """
        Generates and returns the hash values for the given word.
        :param word: The word to be hashed
        :return: List of hash values after applied to the word
        
        >>> len(tf.generate_hashes("hello")) == tf.hash_count
        True
        """
        hashes = []
        i = 2

        hashes.append(self.get_base_hash(word))

        for j in range(1, self.hash_count):
            new_hash = (hashes[j - 1] + (i * hashes[(0 if (j - 2) < 0 else (j - 2))])) % self.length
            i += 1
            hashes.append(new_hash)

        return hashes


    # Calculation
    @staticmethod
    def estimate_optimal_values(n, p):
        """
        
        :param n: number of elements in the set
        :param p: expected rate of false positives , a value between 0 and 1
        :return m, k: the size of the bit array and number of hashes to get desired false positives
        
        >>> isinstance(tf.estimate_optimal_values(1,0.1),tuple)
        True
        >>> tf.estimate_optimal_values(0,0.0)
        Traceback (most recent call last):
        ...
        Exception: Incorrect values for n and k
        """

        if n > 0 and p > 0:

            m = -(n * math.log(p, math.e)) / (math.log(2, math.e) ** 2)
            optimal_hash_count = (m/n) * math.log(2, math.e)
            return abs(math.ceil(m)),abs(math.ceil(optimal_hash_count))

        raise Exception("Incorrect values for n and k")

if __name__ == "__main__":
    import doctest

    doctest.testmod(extraglobs={'tf': BloomFilter(2000, 3)})
