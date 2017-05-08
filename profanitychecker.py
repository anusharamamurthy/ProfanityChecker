import bloomfilter as bloom
import os
import pickle
import string

# Stop words to remove during processing of text.
# Some are taken from the internet
# https://github.com/Alir3z4/python-stop-words
stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'arent', 'as',
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
    """
    Flags comments/reviews containing Obscene words using a bloom filter.
    """
    file_name_suffix = ".bloom"

    def __init__(self, file_name, cached=False, bloom_filter_size=2000, hash_count=3, desired_error_rate=0.01):
        """
        :param file_name: Name of the file containing obscene words
        :param bloom_filter_size: size of the bit array
        :param hash_count: number of hashes to be used
        """
        self.cached = cached
        self.error_rate = desired_error_rate
        self.set_up(file_name.rstrip(os.sep), bloom_filter_size, hash_count)

    def get_words(self, file_name):
        """
        
        :param file_name: Some are taken from the internet - https://gist.github.com/jamiew/1112488
        :return list: A list of all words
        """

        with open(file_name, 'r') as file:
            return [line for line in file]

    def pickle_filter(self, file_name):
        """
        
        :param file_name:name of file to be pickled 
        :return None: 
        """

        pkl = open(file_name, 'wb')
        pickle.dump(self.myFilter, pkl)
        pkl.close()

    def unpickle_filter(self, file_name):
        """
        
        :param file_name: pickled file
        :return None: 
        """

        pkl = open(file_name, 'rb')
        self.myFilter = pickle.load(pkl)
        pkl.close()

    def set_up(self, file_name, filter_size, hash_count):

        """
        :param file_name: File containing obscene words
        :param filter_size: size of the bit array
        :param hash_count: number of hashes
        :return None: 
        """
        if self.cached and file_name + self.file_name_suffix in os.listdir(os.curdir):
            print("Retrieve from the cache")
            self.unpickle_filter(file_name + self.file_name_suffix)
            return None

        words = self.get_words(file_name)  # "profanity_en.txt"
        size,count = bloom.BloomFilter.estimate_optimal_values(len(words),self.error_rate)
        self.myFilter = bloom.BloomFilter(size * 10, count)

        for word in words:
            self.myFilter.insert(word.strip().lower())

        self.pickle_filter(file_name + self.file_name_suffix)

    def sanitize_content(self, content):

        """
        :param content: A list of text
        :return list: A list of words without punctuation and stop words
        
        >>> tf.sanitize_content("")
        []
        >>> tf.sanitize_content("k.e.y.s.$%%&% where is what")
        ['keys']
        """

        content = content.lower()
        rmv_chars = string.punctuation + '\t\n'
        translator = str.maketrans('', '', rmv_chars)
        content = content.translate(translator)
        sanitized_content = [word for word in content.split() if word not in stop_words and len(word) > 2]
        return sanitized_content

    def test_membership(self, text):
        """
        :param text: A string of words
        :return flagged: A list of all words that are flagged for obscenity  
        
        >>> isinstance(tf.test_membership("bs,careless, gladiator, alligator"),list)
        True
        """
        flagged = []
        parsed_text = self.sanitize_content(text)

        for word in parsed_text:
            if self.myFilter.is_member(word):
                flagged.append(word)

        return flagged

if __name__ == "__main__":
    import doctest

    doctest.testmod(extraglobs={'tf': ProfanityChecker("profanity_en.txt")})
