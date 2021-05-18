import bitarray
import mmh3
import math


class BloomFilter(object):

    def __init__(self, item_counts, fp_prob):
        """
        :param item_counts: Number of items expected to store in the filter
        :param fp_prob: The probability of false positive
        """
        # False possible probability in decimal
        self.fp_prob = fp_prob
        # Size of bloom filter array
        self.size = self.get_size(item_counts, fp_prob)

        # Number of Hash functions
        self.k = self.get_hash_count(item_counts, self.size)

        # Initialize filter's bitarray
        self.bit_array = bitarray.bitarray(self.size)

        self.bit_array.setall(0)

    def insert(self, item):
        """
        Add item to the bloom filter array
        """
        for i in range(self.k):
            digest = mmh3.hash(item, i) % self.size

            self.bit_array[digest] = True

    def check(self, item):
        """
        Check if the existence of the item
        :param item:
        :return:
        """
        for i in range(self.k):
            digest = mmh3.hash(item, i) % self.size
            if not self.bit_array[digest]:
                return False
        return True

    @staticmethod
    def get_size(n, p):
        """
        m = -((n*ln(p))/(ln(2)^2))
        :param n: the number of items expected to store in the filter
        :param p: false positive rate
        :return: m
        """
        # Optimal size:
        m = -(n * math.log(p) / math.log(2) ** 2)
        return int(m)

    @staticmethod
    def get_hash_count(n, m):
        """
        K = (m/n) * ln(2)
        :param n: the number of items expected to store in the filter
        :param m: the size of filter
        :return: k
        """
        # Optimal number of hash functions:
        k = (m / n) * math.log(2)
        return int(k)
